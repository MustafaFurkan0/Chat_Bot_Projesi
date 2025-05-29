from veritabani_yonetici import veritabani_guncelleme_yap, veritabani_sorulari_listele
from chroma_yonetici import soru_cevapla, client, soru_ekle, teknik_soru_mu
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils.logger import logger
from typing import Optional

load_dotenv(dotenv_path="openai.env")
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def openai_soru_cevapla(soru: str, kategori: Optional[str] = None) -> Optional[str]:
    """OpenAI API ile teknik soruları cevaplar"""
    try:
        if teknik_soru_mu(soru, kategori) == False:
            return "⚠️ Bu soru teknik bir içeriğe sahip değil. Lütfen teknik bir soru sorun."
        
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content":  """
                    Sen bir teknik destek asistanısın.
                    Görevin:
                    1. Kullanıcının sorduğu sorunun teknik bir konu içerip içermediğini analiz etmek.
                    2. Eğer soru teknikse, kısa, net ve doğrudan teknik bir yanıt ver.
                    3. Eğer soru teknik değilse, teknik olmayan sorulara cevap vermediğini belirten bir uyarı mesajı döndür.
                    Kurallar:
                    - Yanıtlarında selamlaşma, kişisel yorum, gereksiz açıklama veya öneri yer alma.
                    - Sadece teknik açıklamalar yap.
                    - Yanıtlar Türkçe ve profesyonel dille olmalı."""},
                {"role": "user", "content": soru}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"OpenAI hatası: {e}")
        return None

def openai_teknik_soru_cevapla(soru: str) -> Optional[str]:
    """OpenAI API ile teknik soruları cevaplar"""
    try:
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": """Sen bir teknik destek uzmanısın. Kullanıcı bu sorunun cevabından memnun kalmamış o yüzden tekrar araştırman lazım.
                    "Cevapların daha açıklayıcı, net, doğrudan ve teknik dille yazılmalı. Gereksiz açıklama, öneri veya selamlaşma ekleme. "
                - Yanıtlarını Türkçe ver"""},
                {"role": "user", "content": soru}
            ],
            temperature=0.5,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI hatası: {e}")
        return None

def otomatik_kurulum(dosya_yolu: str = "veri_dosyasi.csv"):
    """Sistem başlangıç kurulumunu yapar"""
    try:
        from chroma_yonetici import soru_koleksiyonu_getir
        koleksiyon = soru_koleksiyonu_getir()
        
        if koleksiyon.count() == 0:
            logger.info("Veritabanı boş - yükleme yapılıyor")
            veritabani_guncelleme_yap(dosya_yolu)
        else:
            logger.info("Veritabanında veri mevcut - yükleme atlandı")
    except Exception as e:
        logger.critical(f"Kurulum hatası: {e}")
        raise

def main():
    """Konsol arayüzü için ana fonksiyon"""
    print("🚀 ChatBot başlatılıyor...")
    otomatik_kurulum()

    while True:
        soru = input("\nSorunuz (q=çıkış, data=liste, refresh=yenile): ").strip()
        
        if soru.lower() == 'q':
            break
        elif soru.lower() == 'data':
            for item in veritabani_sorulari_listele():
                print(f"\n[{item['kategori']}] {item['soru']}\n{item['cevap']}")
            continue
        elif soru.lower() == 'refresh':
            client.delete_collection(name="soru_cevap")
            veritabani_guncelleme_yap()
            continue

        cevap, benzer_soru, benzerlik = soru_cevapla(soru)
        
        if benzerlik >= 75:
            print(f"\n🔍 Benzer Soru: {benzer_soru}")
            print(f"📊 Benzerlik: %{benzerlik}")
            print(f"🧠 Cevap: {cevap}")
        else:
            print("\n⚠️ Yerel veritabanında cevap bulunamadı. OpenAI'ya soruluyor...")
            openai_cevap = openai_soru_cevapla(soru)
            if openai_cevap:
                print(f"\n🤖 OpenAI Cevabı:\n{openai_cevap}")
                soru_ekle(soru, openai_cevap, {"source": "openai"})
            else:
                print("OpenAI'dan cevap alınamadı.")

if __name__ == "__main__":
    main()