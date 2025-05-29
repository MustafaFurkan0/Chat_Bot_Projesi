from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from chroma_yonetici import soru_cevapla, soru_ekle
from chat_bot import openai_soru_cevapla, openai_teknik_soru_cevapla
import logging

router = APIRouter(prefix="/api/landbot", tags=["Landbot"])
logger = logging.getLogger(__name__)

class LandbotRequest(BaseModel):
    current_step: str  # "again_question_answering" veya "question_answering"
    selected_category: Optional[str] = None
    user_question: Optional[str] = None

@router.post("/interactive")
async def interactive_handler(request: LandbotRequest):
    logger.info(f"Gelen Landbot isteği: {request}")
    
    category = request.selected_category or "genel"
    question = request.user_question
    
    if request.current_step == "again_question_answering":
        return handle_again_question_answering(question)
    elif request.current_step == "question_answering":
        return handle_question_answering(category, question)
    else:
        raise HTTPException(status_code=400, detail="Geçersiz adım")

def handle_again_question_answering(question: str):
    openai_answer = openai_teknik_soru_cevapla(question)
    response = {
        "messages": [
            {
                "type": "text",
                "content": f"🤖 OpenAI cevabı: {openai_answer}"
            },
        ]
    }
    return response

def handle_question_answering(category: str, question: str):
    if not category:
        category = "genel"
        
    logger.info(f"Kategori: {category}, Soru: {question}")

    answer, similar_q, confidence = soru_cevapla(question, where={"category": category})

    if confidence >= 70:
        response = {
            "messages": [
                {
                    "type": "text",
                    "content": f"[ChromaDB] {answer}"
                },               
            ]
        }
        logger.info(f"Cevap: {answer}")
    else:
        openai_answer = openai_soru_cevapla(question,category)
        response = {
            "messages": [
                {
                    "type": "text",
                    "content": f"[OpenAI] {openai_answer}"
                },
            ]
        }
        soru_ekle(question, openai_answer, category)
        logger.info(f"Cevap: {openai_answer}")
        
    return response
