from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import landbot, admin
from chat_bot import otomatik_kurulum
import logging

# Log ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Teknik Chatbot API", version="1.0.0")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(landbot.router)
app.include_router(admin.router)

# Başlangıçta veritabanını yükle
@app.on_event("startup")
async def startup_event():
    logger.info("Veritabanı yükleme başlatılıyor...") 
    otomatik_kurulum()
    logger.info("Veritabanı yükleme tamamlandı") 

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "running"}