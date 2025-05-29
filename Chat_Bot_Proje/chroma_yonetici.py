from chromadb import HttpClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import hashlib
from typing import Tuple, Optional, Dict
from utils.logger import logger
import re
import string

def teknik_soru_mu(soru: str, kategori: str) -> bool:
    kategori_anahtar_kelimeler = {
        "Yapay Zeka": [
            # Temel ve gelişmiş yapay zeka terimleri
            "yapay zeka", "makine öğrenmesi", "derin öğrenme", "sinir ağı", "denetimli öğrenme",
            "denetimsiz öğrenme", "reinforcement learning", "bias", "variance", "k-means", "kmeans",
            "random forest", "overfitting", "cross-validation", "feature extraction", "epoch",
            "batch size", "transfer learning", "gradient descent", "model tuning",
            "etik", "doğal dil işleme", "autoencoder", "clustering", "tokenization", "attention",
            "transformer", "prompt engineering", "embedding", "llm", "fine-tuning", "unsupervised",

            # Yazılım altyapısı (AI projelerinde sık kullanılanlar)
            "python", "java", "linux", "api", "server", "istemci", "kod", "hata", "bug",
            "veritabanı", "database", "sql", "html", "css", "javascript", "framework",
            "dosya", "sistem", "class", "object", "model", "endpoint", "json", "get", "post",
            "refactoring", "design pattern", "unit test", "ci/cd", "git", "docker", "microservices",
            "restful", "orm", "dependency",

            # Yeni eklemeler - AI ve veri odaklı
            "tensorflow", "pytorch", "keras", "scikit-learn", "data augmentation", "hyperparameter tuning",
            "neural network", "backpropagation", "cnn", "rnn", "gan", "svm", "feature scaling", "data preprocessing",
            "accuracy", "precision", "recall", "f1-score"
        ],
        "Siber Güvenlik": [
            # Temel güvenlik terimleri
            "phishing", "firewall", "ddos", "sql injection", "xss", "hashleme",
            "penetrasyon testi", "ids", "zero-day", "ransomware", "antivirüs",
            "sosyal mühendislik", "2fa", "brute force", "man-in-the-middle",
            "log analizi", "red team", "blue team", "malware", "exploit", "rootkit", "cyberattack", "forensics",
            "zero trust", "siem", "mitre att&ck", "sandbox", "privilege escalation",

            # Ağ ve sistem güvenliği
            "donanım", "yazılım", "port", "ip", "socket", "thread", "ağ", "network", "vpn","linux",

            # Yeni eklemeler - güncel ve ileri seviye
            "sandboxing", "zero trust architecture", "security operations center", "SOC",
            "vulnerability scanning", "patch management", "threat hunting", "incident response",
            "cryptography", "encryption", "decryption", "public key", "private key",
            "multi-factor authentication", "MFA", "privilege management", "SIEM", "DLP", "IDS", "IPS",
            "cyber threat intelligence", "CTI", "SOC analyst"
        ]
    }
    
    soru = soru.lower()
    
    anahtar_kelimeler = kategori_anahtar_kelimeler.get(kategori)
    if not anahtar_kelimeler:
        return False  # Geçersiz kategori durumunda False döndür
    
    return any(kelime in soru for kelime in anahtar_kelimeler)

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

# ChromaDB bağlantısı
try:
    client = HttpClient(host="localhost", port=8001)
    logger.info("ChromaDB'ye bağlanıldı")
except Exception as e:
    logger.critical(f"ChromaDB bağlantı hatası: {e}")
    raise

# Embedding modeli
try:
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    logger.info("Embedding modeli yüklendi")
except Exception as e:
    logger.critical(f"Model yükleme hatası: {e}")
    raise

def soru_koleksiyonu_getir():
    """ChromaDB koleksiyonunu getirir veya oluşturur"""
    try:
        return client.get_or_create_collection(
            name="soru_cevap",
            metadata={"hnsw:space": "cosine"}
        )
    except Exception as e:
        logger.error(f"Koleksiyon hatası: {e}")
        raise

def satir_id_hesapla(metin: str) -> str:
    """Metnin benzersiz ID'sini oluşturur"""
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()

def soru_cevapla(
    soru: str,
    where: Optional[Dict] = None,
    benzerlik_esigi: float = 0.75
) -> Tuple[str, str, float]:
    """Geliştirilmiş soru cevaplama fonksiyonu"""
    try:
        koleksiyon = soru_koleksiyonu_getir()
        processed_soru = preprocess_text(soru)
        embedding = model.encode(processed_soru).tolist()
        
        sonuc = koleksiyon.query(
            query_embeddings=[embedding],
            n_results=1,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        if sonuc and sonuc["documents"]:
            benzerlik = 1 - sonuc['distances'][0][0]
            if benzerlik >= benzerlik_esigi:
                meta = sonuc['metadatas'][0][0]
                return (
                    sonuc['documents'][0][0],
                    meta.get('question', soru),
                    round(benzerlik * 100, 2)
                )
        
        return "", "", 0.0
        
    except Exception as e:
        logger.error(f"Soru cevaplama hatası: {e}")
        return "", "", 0.0

def soru_ekle(soru: str, cevap: str, kategori: str, metadata: Optional[Dict] = None):
    """ChromaDB'ye yeni soru-cevap ve kategori ekler."""
    try:
        koleksiyon = soru_koleksiyonu_getir() 
        soru_id = satir_id_hesapla(soru)      
        
        # Temel metadata'yı soru ve varsayılan kaynak ile başlat
        current_meta = {
            "question": soru,
            "source": "manual"
        }
        
        if metadata:
            current_meta.update(metadata)
        
        current_meta["category"] = kategori
        
        koleksiyon.add(
            documents=[cevap],
            embeddings=[model.encode(preprocess_text(soru)).tolist()], 
            metadatas=[current_meta],
            ids=[soru_id]
        )
        logger.info(f"Soru eklendi (Kategori: {kategori}): {soru[:50]}...")
        
    except Exception as e:
        logger.error(f"Soru ekleme hatası: {e}")
        raise 