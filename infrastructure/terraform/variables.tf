/**
 * variables.tf
 * 
 * Переменные для Terraform конфигурации
 * 
 * Copyright (c) 2023 Nick Scherbakov
 * Licensed under the MIT License
 */

variable "yc_token" {
  description = "Yandex Cloud API токен"
  type        = string
  sensitive   = true
}

variable "yc_cloud_id" {
  description = "Идентификатор облака в Yandex Cloud"
  type        = string
}

variable "yc_folder_id" {
  description = "Идентификатор каталога в Yandex Cloud"
  type        = string
}

variable "yc_zone" {
  description = "Зона доступности Yandex Cloud"
  type        = string
  default     = "ru-central1-a"
}
