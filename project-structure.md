# Структура проекта textbook-explainer

```
textbook-explainer/
├── .github/                      # GitHub-специфичные файлы
│   ├── workflows/                # CI/CD workflows для GitHub Actions
│   │   ├── deploy.yml            # Деплой в Yandex Cloud
│   │   └── test.yml              # Тестирование кода
├── docs/                         # Документация проекта
│   ├── architecture.md           # Архитектурная документация
│   ├── api.md                    # API-документация
│   └── user-guide.md             # Руководство пользователя
├── infrastructure/               # Инфраструктурные файлы
│   ├── docker-compose.yml        # Конфигурация Docker Compose для локальной разработки
│   ├── kubernetes/               # Kubernetes-манифесты
│   │   ├── deployments/          # Деплойменты сервисов
│   │   ├── services/             # Сервисы Kubernetes
│   │   └── config-maps/          # Конфигурационные карты
│   └── terraform/                # Terraform-скрипты для Yandex Cloud
├── services/                     # Микросервисы
│   ├── upload-service/           # Сервис загрузки и хранения файлов
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
│   ├── ocr-service/              # Сервис OCR с использованием Vision API
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
│   ├── nlp-service/              # Сервис обработки текста (YandexGPT)
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
│   ├── dialog-service/           # Сервис диалогов
│   │   ├── Dockerfile
│   │   ├── src/
│   │   └── requirements.txt
│   └── voice-service/            # Сервис голосового интерфейса
│       ├── Dockerfile
│       ├── src/
│       └── requirements.txt
├── frontend/                     # Фронтенд-приложение
│   ├── Dockerfile
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── shared/                       # Общие библиотеки и утилиты
│   ├── models/                   # Общие модели данных
│   └── utils/                    # Утилиты для работы с Yandex Cloud
├── .gitignore                    # Файлы/директории для игнорирования Git
├── docker-compose.yml            # Основной Docker Compose файл
├── README.md                     # Основной README файл проекта
├── manifest-ru.md                # Русскоязычный манифест проекта
└── LICENSE                       # Лицензия проекта
```

## Микросервисы

### upload-service
Сервис для загрузки файлов, интеграции с Yandex Object Storage и очередями сообщений.

### ocr-service
Сервис для распознавания текста из изображений и PDF с использованием Yandex Vision API.

### nlp-service
Сервис для обработки и упрощения текста с использованием YandexGPT.

### dialog-service
Сервис для обработки диалогового взаимодействия с использованием Yandex Dialogs.

### voice-service
Сервис для обработки голосового ввода/вывода с использованием Yandex SpeechKit.

## Frontend
Веб-приложение для пользовательского взаимодействия с системой.

## Инфраструктура
Содержит конфигурационные файлы для развертывания в Yandex Cloud с использованием Docker, Kubernetes и Terraform.
