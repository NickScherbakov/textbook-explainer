/**
 * main.tf
 * 
 * Основной файл terraform для развертывания инфраструктуры textbook-explainer в Yandex Cloud
 * 
 * Copyright (c) 2023 Nick Scherbakov
 * Licensed under the MIT License
 */

terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
      version = "~> 0.82.0"
    }
  }

  backend "s3" {
    endpoint   = "storage.yandexcloud.net"
    bucket     = "textbook-explainer-terraform-state"
    region     = "ru-central1"
    key        = "terraform.tfstate"
    
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = var.yc_zone
}

# Сеть и подсети
resource "yandex_vpc_network" "network" {
  name = "textbook-explainer-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "textbook-explainer-subnet"
  zone           = var.yc_zone
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.2.0.0/16"]
}

# Сервисный аккаунт для Kubernetes
resource "yandex_iam_service_account" "k8s_account" {
  name        = "k8s-service-account"
  description = "Service account для управления Kubernetes кластером"
}

# Назначение роли сервисному аккаунту
resource "yandex_resourcemanager_folder_iam_binding" "k8s_account_binding" {
  folder_id = var.yc_folder_id
  role      = "editor"
  members   = [
    "serviceAccount:${yandex_iam_service_account.k8s_account.id}",
  ]
}

# Создание Kubernetes кластера
resource "yandex_kubernetes_cluster" "k8s_cluster" {
  name       = "textbook-explainer-cluster"
  description = "Kubernetes кластер для textbook-explainer"
  
  network_id = yandex_vpc_network.network.id
  
  master {
    version = "1.22"
    zonal {
      zone      = var.yc_zone
      subnet_id = yandex_vpc_subnet.subnet.id
    }
    
    public_ip = true
    
    maintenance_policy {
      auto_upgrade = true
      
      maintenance_window {
        start_time = "02:00"
        duration   = "3h"
      }
    }
  }
  
  service_account_id      = yandex_iam_service_account.k8s_account.id
  node_service_account_id = yandex_iam_service_account.k8s_account.id
  
  release_channel = "REGULAR"
  
  depends_on = [
    yandex_resourcemanager_folder_iam_binding.k8s_account_binding
  ]
}

# Группа узлов для сервисов
resource "yandex_kubernetes_node_group" "services_node_group" {
  cluster_id = yandex_kubernetes_cluster.k8s_cluster.id
  name       = "services-node-group"
  version    = "1.22"
  
  instance_template {
    platform_id = "standard-v2"
    
    resources {
      memory = 8
      cores  = 4
    }
    
    boot_disk {
      type = "network-hdd"
      size = 64
    }
    
    network_interface {
      subnet_ids = [yandex_vpc_subnet.subnet.id]
    }
    
    scheduling_policy {
      preemptible = false
    }
  }
  
  scale_policy {
    auto_scale {
      min     = 3
      max     = 6
      initial = 3
    }
  }
  
  allocation_policy {
    location {
      zone = var.yc_zone
    }
  }
  
  maintenance_policy {
    auto_upgrade = true
    auto_repair  = true
    
    maintenance_window {
      day        = "monday"
      start_time = "02:00"
      duration   = "3h"
    }
  }
}

# S3 бакет для хранения данных
resource "yandex_storage_bucket" "storage_bucket" {
  bucket     = "textbook-explainer-storage"
  acl        = "private"
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    enabled = true
    
    expiration {
      days = 365
    }
    
    noncurrent_version_expiration {
      days = 30
    }
  }
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# База данных PostgreSQL
resource "yandex_mdb_postgresql_cluster" "postgres_db" {
  name        = "textbook-explainer-db"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.network.id
  
  config {
    version = "14"
    resources {
      resource_preset_id = "s2.micro"
      disk_type_id       = "network-ssd"
      disk_size          = 20
    }
  }
  
  host {
    zone      = var.yc_zone
    subnet_id = yandex_vpc_subnet.subnet.id
  }
}
