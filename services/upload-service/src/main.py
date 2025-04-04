import os
import boto3
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Upload Service")

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройки для подключения к Yandex Object Storage
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('YANDEX_CLOUD_KEY_ID'),
    aws_secret_access_key=os.environ.get('YANDEX_CLOUD_SECRET'),
    endpoint_url='https://storage.yandexcloud.net'
)

BUCKET_NAME = os.environ.get('YANDEX_CLOUD_STORAGE_BUCKET', 'textbook-explainer-storage')

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    storage_path: str
    status: str = "uploaded"

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Загрузка документа в Yandex Object Storage"""
    try:
        # Генерация уникального идентификатора для документа
        document_id = str(uuid.uuid4())
        
        # Определение пути хранения в бакете
        storage_path = f"documents/{document_id}/{file.filename}"
        
        # Загрузка файла в Yandex Object Storage
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            storage_path
        )
        
        # Отправка сообщения в очередь для дальнейшей обработки (OCR)
        # TODO: Добавить код для работы с очередью сообщений
        
        return DocumentResponse(
            document_id=document_id,
            filename=file.filename,
            storage_path=storage_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки: {str(e)}")

@app.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Получение информации о документе по его ID"""
    # В реальном приложении здесь будет запрос к базе данных
    # Заглушка для примера
    return DocumentResponse(
        document_id=document_id,
        filename="example.pdf",
        storage_path=f"documents/{document_id}/example.pdf"
    )

@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy"}
