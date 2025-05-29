import os
import hashlib
import pandas as pd
from chroma_yonetici import soru_ekle, soru_koleksiyonu_getir, satir_id_hesapla
from utils.logger import logger

def veritabani_hash_hesapla(dosya_yolu: str = "veri_dosyasi.csv") -> str:
    """Veritabanı dosyasının hash'ini hesaplar"""
    try:
        with open(dosya_yolu, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.error(f"Hash hesaplama hatası: {e}")
        return ""

def veritabani_guncelleme_yap(dosya_yolu: str = "veri_dosyasi.csv") -> bool:
    """Veritabanını günceller ve kategorileri işler"""
    try:
        hash_dosya = "chroma_hash.txt"
        mevcut_hash = veritabani_hash_hesapla(dosya_yolu)
        
        if os.path.exists(hash_dosya):
            with open(hash_dosya, "r") as f:
                onceki_hash = f.read().strip()
        else:
            onceki_hash = ""
        
        koleksiyon = soru_koleksiyonu_getir()
        if mevcut_hash == onceki_hash and koleksiyon.count() > 0:
            logger.info("Veritabanı güncel - yükleme yapılmadı")
            return True

        logger.info("Veritabanı güncelleniyor...")
        df = pd.read_csv(dosya_yolu)
        
        # Sütun kontrolü ve temizlik
        required_cols = ['question', 'answer']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV dosyasında {required_cols} sütunları olmalıdır")
        
        df = df.dropna(subset=required_cols)
        df = df.drop_duplicates(subset=['question'])
        df['category'] = df.get('category', 'genel')
        
        mevcut_idler = set(koleksiyon.get()['ids'])
        added = 0
        
        for _, row in df.iterrows():
            soru = str(row['question']).strip()
            cevap = str(row['answer']).strip()
            kategori = str(row['category']).strip()
            
            if soru and cevap:
                soru_id = satir_id_hesapla(soru)
                if soru_id not in mevcut_idler:
                    soru_ekle(soru, cevap, {"category": kategori, "question": soru})
                    added += 1
        
        with open(hash_dosya, "w") as f:
            f.write(mevcut_hash)
        
        logger.info(f"{added} yeni soru eklendi")
        return True
        
    except Exception as e:
        logger.error(f"Güncelleme hatası: {e}")
        return False

def veritabani_sorulari_listele(kategori: str = None):
    """Veritabanındaki soruları listeler (opsiyonel kategori filtresi)"""
    try:
        koleksiyon = soru_koleksiyonu_getir()
        where = {"category": kategori} if kategori else None
        
        results = koleksiyon.get(where=where)
        if not results['documents']:
            logger.info("Kayıtlı soru bulunamadı")
            return []
        
        return [
            {
                "soru": meta['question'],
                "cevap": doc,
                "kategori": meta.get('category', 'genel')
            }
            for meta, doc in zip(results['metadatas'], results['documents'])
        ]
        
    except Exception as e:
        logger.error(f"Listeleme hatası: {e}")
        return []