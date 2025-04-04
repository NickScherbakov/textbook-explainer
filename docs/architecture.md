# Архитектура textbook-explainer

## Обзор

Проект textbook-explainer реализован как набор взаимодействующих микросервисов, каждый из которых отвечает за отдельную функциональную область. Такая архитектура обеспечивает гибкость, масштабируемость и отказоустойчивость.

## Схема взаимодействия компонентов

```
                   +------------------------+
                   |      Пользователь      |
                   | (Веб/мобильное приложение)  |
                   +-----------+------------+
                               |
                               v
                   +-----------+------------+
                   |  API Gateway / LB      |
                   +-----------+------------+
                               |
              +----------------+-------------------+
              |                |                   |
              v                v                   v
   +----------------+  +----------------+   +---------------------+
   | Модуль загрузки|  |  Модуль диалога|   | Модуль голосового   |
   |  & регистрации |  | (Yandex Dialogs)|   | ввода/вывода        |
   +-------+--------+  +-------+--------+   +---------+-----------+
           |                   |                        |
           v                   v                        |
   +---------------+    +---------------+                |
   | Yandex Object |<---+  Очередь      |<---------------+
   |   Storage     |    | (Message Queue)|
   +---------------+    +---------------+
           |
           v
  +------------------------+
  | Модуль OCR (Vision API)|
  +-----------+------------+
              |
              v
  +-----------------------------+
  | Модуль обработки текста     |
  | (YandexGPT, NLP, Translate) |
  +-------------+---------------+
                |
                v
  +------------------------------+
  |   Хранилище результатов      |
  | (PostgreSQL, DataSphere)     |
  +------------------------------+
```

## Компоненты системы

### Frontend (Пользовательский интерфейс)
- Веб-приложение для загрузки документов, просмотра и взаимодействия с обработанными материалами
- Реализовано с использованием современных фреймворков (React, Vue.js)
- Взаимодействует с бэкенд-сервисами через RESTful API

### upload-service (Сервис загрузки)
- Отвечает за прием и сохранение файлов
- Интегрируется с Yandex Object Storage для хранения документов
- Отправляет сообщения в очередь для последующей обработки

### ocr-service (Сервис OCR)
- Распознает текст в загруженных документах с помощью Yandex Vision API
- Обрабатывает различные форматы (PDF, изображения)
- Структурирует и подготавливает текст для обработки в NLP-сервисе

### nlp-service (Сервис NLP)
- Анализирует и упрощает текст с помощью YandexGPT
- Генерирует объяснения сложных концепций
- Адаптирует содержание под разные уровни сложности

### dialog-service (Сервис диалогов)
- Обеспечивает интерактивное взаимодействие в формате вопрос-ответ
- Интегрируется с Yandex Dialogs для обработки пользовательских запросов
- Использует контекст документа для генерации релевантных ответов

### voice-service (Сервис голосового взаимодействия)
- Преобразует голосовые запросы в текст с помощью Yandex SpeechKit
- Озвучивает ответы системы
- Обеспечивает мультимодальное взаимодействие

## Безопасность и масштабирование

### Безопасность
- Аутентификация и авторизация на основе IAM Yandex Cloud
- Шифрование данных при передаче (TLS) и хранении
- Регулярное обновление зависимостей и мониторинг уязвимостей

### Масштабирование
- Горизонтальное масштабирование микросервисов в Kubernetes
- Автоматическое масштабирование на основе нагрузки
- Асинхронная обработка через очереди сообщений для равномерного распределения нагрузки

## Хранение данных
- Документы хранятся в Yandex Object Storage
- Метаданные и структурированные результаты в PostgreSQL
- Аналитика и большие данные обрабатываются с помощью DataSphere

## Мониторинг и логирование
- Сбор метрик и логов с помощью Yandex Monitoring и Yandex Logging
- Визуализация метрик в Grafana
- Настроенные оповещения о проблемах и аномалиях
