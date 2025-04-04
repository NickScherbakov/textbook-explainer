# API документация textbook-explainer

## Обзор API

Наш API построен на REST принципах и использует стандартные HTTP методы. Ответы возвращаются в формате JSON. Все эндпоинты требуют авторизации с использованием токена доступа Yandex Cloud IAM.

## Базовый URL

```
https://api.textbook-explainer.example.com/v1
```

## Аутентификация

Для аутентификации используйте HTTP заголовок `Authorization` со значением `Bearer <ваш-токен>`:

```
Authorization: Bearer yc.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Эндпоинты

### Управление документами

#### Загрузка документа

**Запрос:**

```http
POST /documents
Content-Type: multipart/form-data

file=@path/to/document.pdf
target_audience=student
complexity_level=2
```

**Ответ:**

```json
{
  "document_id": "doc_12345",
  "filename": "document.pdf",
  "storage_path": "documents/doc_12345/document.pdf",
  "status": "uploaded",
  "created_at": "2023-11-01T12:34:56Z"
}
```

#### Получение информации о документе

**Запрос:**

```http
GET /documents/{document_id}
```

**Ответ:**

```json
{
  "document_id": "doc_12345",
  "filename": "document.pdf",
  "storage_path": "documents/doc_12345/document.pdf",
  "status": "processed",
  "created_at": "2023-11-01T12:34:56Z",
  "processed_at": "2023-11-01T12:36:23Z",
  "page_count": 5,
  "sections": [
    {
      "section_id": "section_1",
      "title": "Введение",
      "original_text_url": "https://storage.yandexcloud.net/textbook-explainer/doc_12345/original/section_1.txt",
      "simplified_text_url": "https://storage.yandexcloud.net/textbook-explainer/doc_12345/simplified/section_1.txt"
    }
  ]
}
```

### OCR и обработка текста

#### Запуск OCR для документа

**Запрос:**

```http
POST /documents/{document_id}/ocr
Content-Type: application/json

{
  "language": "ru",
  "extract_tables": true
}
```

**Ответ:**

```json
{
  "job_id": "ocr_job_67890",
  "status": "processing",
  "document_id": "doc_12345",
  "created_at": "2023-11-01T12:35:12Z"
}
```

#### Получение результатов OCR

**Запрос:**

```http
GET /documents/{document_id}/ocr
```

**Ответ:**

```json
{
  "document_id": "doc_12345",
  "status": "completed",
  "pages": [
    {
      "page_number": 1,
      "text": "Полный текст, извлеченный из страницы...",
      "tables": [
        {
          "rows": 3,
          "columns": 4,
          "data": [...]
        }
      ],
      "confidence": 0.97
    }
  ],
  "created_at": "2023-11-01T12:35:12Z",
  "completed_at": "2023-11-01T12:35:45Z"
}
```

### Упрощение текста

#### Запуск упрощения текста

**Запрос:**

```http
POST /documents/{document_id}/simplify
Content-Type: application/json

{
  "target_audience": "student",
  "complexity_level": 2,
  "sections": ["section_1", "section_2"]
}
```

**Ответ:**

```json
{
  "job_id": "simplify_job_54321",
  "status": "processing",
  "document_id": "doc_12345",
  "created_at": "2023-11-01T12:36:01Z"
}
```

#### Получение результатов упрощения

**Запрос:**

```http
GET /documents/{document_id}/simplified
```

**Ответ:**

```json
{
  "document_id": "doc_12345",
  "status": "completed",
  "sections": [
    {
      "section_id": "section_1",
      "title": "Введение",
      "original_text": "Исходный сложный текст...",
      "simplified_text": "Упрощенная версия текста...",
      "explanations": [
        {
          "concept": "Термодинамика",
          "explanation": "Термодинамика - это наука о тепловой энергии и ее превращениях..."
        }
      ]
    }
  ],
  "created_at": "2023-11-01T12:36:01Z",
  "completed_at": "2023-11-01T12:36:23Z"
}
```

### Интерактивный диалог

#### Задать вопрос по документу

**Запрос:**

```http
POST /documents/{document_id}/ask
Content-Type: application/json

{
  "question": "Объясните подробнее концепцию термодинамики из раздела Введение",
  "context_sections": ["section_1"]
}
```

**Ответ:**

```json
{
  "question_id": "q_13579",
  "question": "Объясните подробнее концепцию термодинамики из раздела Введение",
  "answer": "Термодинамика изучает преобразования энергии, особенно тепловой энергии в механическую работу и наоборот. В документе это объясняется следующим образом...",
  "relevant_sections": ["section_1"],
  "confidence": 0.92,
  "created_at": "2023-11-01T12:37:45Z"
}
```

## Коды состояний HTTP

- `200 OK` - Запрос успешно обработан
- `201 Created` - Ресурс успешно создан
- `400 Bad Request` - Ошибка в параметрах запроса
- `401 Unauthorized` - Отсутствует или недействителен токен авторизации
- `403 Forbidden` - Недостаточно прав для доступа к ресурсу
- `404 Not Found` - Ресурс не найден
- `500 Internal Server Error` - Внутренняя ошибка сервера

## Ограничения

- Максимальный размер загружаемого файла: 50 МБ
- Максимальное количество запросов: 100 запросов в минуту на один API ключ
- Поддерживаемые форматы документов: PDF, PNG, JPEG, TIFF
