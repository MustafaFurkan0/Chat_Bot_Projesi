from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import csv
import logging
from pathlib import Path

# CSV dosyası yolu
SIKAYET_CSV_PATH = Path("sikayet_kayitlari.csv")

# Logger
logger = logging.getLogger(__name__)

# Router tanımı
router = APIRouter(prefix="/api/admin", tags=["Admin"])

# Pydantic modeli
class ComplaintRequest(BaseModel):
    email: str
    isim: str
    soru: str

# CSV’ye log yazan yardımcı fonksiyon
def sikayet_logla(email: str, isim: str, soru: str):
    fieldnames = ["timestamp", "email", "isim", "soru"]
    dosya_mevcut = SIKAYET_CSV_PATH.exists()
    
    try:
        with open(SIKAYET_CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not dosya_mevcut:
                writer.writeheader()
            writer.writerow({
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "email": email,
                "isim": isim,
                "soru": soru
            })
        logger.info(f"Şikayet kaydedildi: {email} - {isim}")
    except Exception as e:
        logger.error(f"Şikayet kaydedilemedi: {e}")
        raise HTTPException(status_code=500, detail="Şikayet kaydı başarısız")

# Endpoint
@router.post("/log")
async def log_complaint(request: ComplaintRequest):
    sikayet_logla(request.email, request.isim, request.soru)
    return {"message": "Şikayet başarıyla kaydedildi"}
