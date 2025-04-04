import os
import requests
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI(title="NLP Service")

# Настройки YandexGPT API
YANDEX_GPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
API_KEY = os.environ.get('YANDEX_GPT_API_KEY')

class NLPRequest(BaseModel):
    document_id: str
    extracted_text: str
    target_audience: Optional[str] = "student"  # student, teacher, researcher
    complexity_level: Optional[int] = 2  # от 1 (просто) до 5 (сложно)

class Section(BaseModel):
    title: str
    original_text: str
    simplified_text: str
    explanations: Optional[List[str]] = []

class NLPResponse(BaseModel):
    document_id: str
    sections: List[Section]
    status: str = "processed"

@app.post("/simplify", response_model=NLPResponse)
async def simplify_text(request: NLPRequest):
    """Упрощение и объяснение текста с помощью YandexGPT"""
    try:
        # Разделение текста на логические секции (параграфы)
        # В реальном приложении здесь будет более сложная логика
        paragraphs = request.extracted_text.split('\n\n')
        
        sections = []
        for i, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                continue
                
            # Формирование запроса к YandexGPT
            prompt = f"""
            Оригинальный текст:
            {paragraph}
            
            Пожалуйста, упрости этот текст для {request.target_audience} и дай подробное объяснение 
            ключевых концепций. Уровень сложности: {request.complexity_level} из 5.
            """
            
            # В реальном приложении здесь будет запрос к YandexGPT API
            # Имитация ответа для примера
            simplified_text = f"Упрощенная версия параграфа {i+1}: {paragraph[:50]}..."
            explanations = [f"Объяснение концепции 1 из параграфа {i+1}", 
                           f"Объяснение концепции 2 из параграфа {i+1}"]
            
            sections.append(Section(
                title=f"Раздел {i+1}",
                original_text=paragraph,
                simplified_text=simplified_text,
                explanations=explanations
            ))
        
        return NLPResponse(
            document_id=request.document_id,
            sections=sections
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки NLP: {str(e)}")

@app.post("/explain-concept")
async def explain_concept(concept: str, context: Optional[str] = None):
    """Объяснение отдельного концепта с помощью YandexGPT"""
    try:
        # Формирование запроса к YandexGPT
        prompt = f"""
        Пожалуйста, дай понятное объяснение концепта: {concept}
        """
        if context:
            prompt += f"\nКонтекст: {context}"
        
        # В реальном приложении здесь будет запрос к YandexGPT API
        # Имитация ответа для примера
        return {
            "concept": concept,
            "explanation": f"Это детальное объяснение концепта '{concept}'..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка объяснения концепта: {str(e)}")

@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy"}
