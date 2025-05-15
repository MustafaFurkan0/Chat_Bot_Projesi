#veritabani_yonetici.py
import os
import hashlib
import pandas as pd
from chroma_yonetici import soru_ekle, soru_koleksiyonu_getir, satir_id_hesapla

def veritabani_hash_hesapla(dosya_yolu: str = "veri_dosyasi.csv") -> str:
    """Veritabanı dosyasının hash'ini hesaplar"""
    try:
        with open(dosya_yolu, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        print(f"❌ Hash hesaplama hatası: {e}")
        return ""

def veritabani_guncelleme_yap(dosya_yolu: str = "veri_dosyasi.csv") -> bool:
    """Veritabanını sadece gerektiğinde günceller"""
    # Hash dosyası kontrolü
    hash_dosya = "chroma_hash.txt"
    mevcut_hash = veritabani_hash_hesapla(dosya_yolu)
    
    if os.path.exists(hash_dosya):
        with open(hash_dosya, "r") as f:
            onceki_hash = f.read().strip()
    else:
        onceki_hash = ""
    
    # Hash değişmemişse ve ChromaDB'de veri varsa işlem yapma
    koleksiyon = soru_koleksiyonu_getir()
    if mevcut_hash == onceki_hash and koleksiyon.count() > 0:
        print("✅ Veritabanı güncel - yükleme yapılmadı")
        return True
    
    try:
        print("\n🔍 Veritabanı güncelleniyor...")
        df = pd.read_csv(dosya_yolu)
        
        # Gerekli sütun kontrolü
        if not all(col in df.columns for col in ['question', 'answer']):
            raise ValueError("CSV dosyasında 'question' ve 'answer' sütunları olmalıdır")
        
        # Temizleme işlemleri
        df = df.dropna(subset=['question', 'answer'])
        df = df.drop_duplicates(subset=['question'])
        
        # Mevcut ID'leri al
        mevcut_idler = set(koleksiyon.get()['ids'])
        total_added = 0
        
        for _, row in df.iterrows():
            soru = str(row['question']).strip()
            cevap = str(row['answer']).strip()
            
            if soru and cevap:
                soru_id = satir_id_hesapla(soru)
                
                if soru_id not in mevcut_idler:
                    soru_ekle(soru, cevap)
                    total_added += 1
        
        # Hash'i kaydet
        with open(hash_dosya, "w") as f:
            f.write(mevcut_hash)
        
        print(f"✅ {total_added} yeni soru-cevap çifti eklendi")
        return True
        
    except Exception as e:
        print(f"❌ Güncelleme hatası: {str(e)}")
        return False

def veritabani_sorulari_listele():
    """ChromaDB'deki tüm soruları listeler"""
    try:
        koleksiyon = soru_koleksiyonu_getir()
        veriler = koleksiyon.get()
        
        if not veriler['documents']:
            print("ℹ️ ChromaDB'de kayıtlı soru bulunamadı")
            return
        
        print("\n📋 ChromaDB'deki Sorular:")
        for i, (metadata, cevap) in enumerate(zip(veriler['metadatas'], veriler['documents']), 1):
            print(f"{i}. Soru: {metadata.get('question', 'Bilinmeyen')}")
            print(f"   Cevap: {cevap[:100]}...\n")
            
    except Exception as e:
        print(f"❌ Listeleme hatası: {e}")