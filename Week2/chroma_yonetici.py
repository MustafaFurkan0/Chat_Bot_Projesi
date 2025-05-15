#chroma_yonetici.py
from chromadb import HttpClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import re
import string
from typing import Tuple
import hashlib

def preprocess_text(text: str) -> str:
    """Metni önişlemeden geçirerek temizler"""
    # Türkçe stopword listesi
    stop_words = {
        "acaba", "ama", "aslında", "az", "bazı", "belki", "biri", "birkaç", 
        "birşey", "biz", "bu", "çok", "çünkü", "da", "de", "defa", "diye", 
        "eğer", "en", "gibi", "hem", "hep", "hepsi", "her", "hiç", "için", 
        "ile", "ise", "kez", "ki", "kim", "mı", "mu", "mü", "nasıl", "ne",
        "neden", "nerde", "nerede", "nereye", "niçin", "niye", "o", "sanki",
        "şey", "siz", "şu", "tüm", "ve", "veya", "ya", "yani", "zaten"
    }

    # Küçük harfe çevirme
    text = text.lower()
    
    # Noktalama temizleme
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Özel karakterler
    text = re.sub(r'[^a-zçğıöşüâîû\s]', '', text)
    
    # Stopword'leri kaldırma ve kısa kelimeleri filtreleme
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]

    return ' '.join(filtered_words)

# ChromaDB bağlantı ayarları
try:
    client = HttpClient(host="localhost", port=8000)
    print("✅ ChromaDB'ye başarıyla bağlanıldı.")
except Exception as e:
    print(f"❌ ChromaDB bağlantı hatası: {e}")
    raise

# Embedding modeli
try:
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    print("✅ Embedding modeli yüklendi.")
except Exception as e:
    print(f"❌ Model yükleme hatası: {e}")
    raise

def soru_koleksiyonu_getir():
    """Soru-yanıt koleksiyonuna erişim sağlar"""
    try:
        return client.get_or_create_collection(
            name="soru_cevap",
            metadata={"hnsw:space": "cosine"}
        )
    except Exception as e:
        print(f"❌ Koleksiyon oluşturma hatası: {e}")
        raise

def satir_id_hesapla(metin: str) -> str:
    """Metnin hash'ini oluşturur"""
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()

def soru_cevapla(soru: str) -> Tuple[str, str, float]:
    """Geliştirilmiş soru cevaplama fonksiyonu"""
    try:
        # Arama için soruyu preprocess et
        processed_soru = preprocess_text(soru)
        koleksiyon = soru_koleksiyonu_getir()
        soru_embedding = model.encode(processed_soru).tolist()
        
        sonuc = koleksiyon.query(
            query_embeddings=[soru_embedding],
            n_results=1,
            include=["documents", "metadatas", "distances"]
        )
        
        if sonuc and sonuc["documents"]:
            benzerlik = 1 - sonuc['distances'][0][0]  # Cosine distance to similarity
            benzerlik_yuzde = round(benzerlik * 100, 2)
            
            # Metadata'dan orijinal soruyu al
            en_yakin_soru = sonuc['metadatas'][0][0].get('question', 'Bilinmeyen Soru')
            cevap = sonuc['documents'][0][0]
            
            return cevap, en_yakin_soru, benzerlik_yuzde
        else:
            return "Üzgünüm, bu soruya bir cevap bulamadım.", "", 0.0
            
    except Exception as e:
        print(f"❌ Soru cevaplama hatası: {e}")
        return "Bir hata oluştu, lütfen tekrar deneyin.", "", 0.0
    
def soru_ekle(soru: str, cevap: str):
    """Yeni soru ve cevabı ChromaDB'ye ekler"""
    try:
        koleksiyon = soru_koleksiyonu_getir()
        soru_id = satir_id_hesapla(soru)
        embedding = model.encode(preprocess_text(soru)).tolist()
        
        koleksiyon.add(
            documents=[cevap],
            embeddings=[embedding],
            metadatas=[{"question": soru}],  # Orijinal soruyu metadata'da sakla
            ids=[soru_id]
        )
        print(f"✅ Yeni soru eklendi: {soru[:50]}...")
        
    except Exception as e:
        print(f"❌ Soru ekleme hatası: {e}")