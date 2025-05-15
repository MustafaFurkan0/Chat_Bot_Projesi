#chat_bot.py
from veritabani_yonetici import veritabani_guncelleme_yap, veritabani_sorulari_listele, soru_ekle
from chroma_yonetici import soru_cevapla, client
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(dotenv_path="openai.env")
client_opeanai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def openai_soru_cevapla(soru):
    """OpenAI API kullanarak teknik sorulara kısa ve net cevaplar verir"""
    try:
        response = client_opeanai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": """Sen bir teknik destek uzmanısın. Kullanıcıların teknik sorularına:
                    "Sadece yazılım, programlama, yapay zeka, siber güvenlik,mühendislik gibi teknik konularda gelen sorulara cevap ver. "
                    "Cevapların kısa, net, doğrudan ve teknik dille yazılmalı. Gereksiz açıklama, öneri veya selamlaşma ekleme. "
                    "Eğer gelen soru teknik değilse, 'Bu sistem yalnızca teknik sorulara cevap verir.' yanıtını ver."
                - Yanıtlarını Türkçe ver"""},
                {"role": "user", "content": soru}
            ],
            temperature=0.5,  # Daha deterministik cevaplar için
            max_tokens=300,   # Daha kısa cevaplar için
            top_p=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI hatası: {str(e)}")
        return None


def otomatik_kurulum(dosya_yolu: str = "veri_dosyasi.csv"):
    """Veritabanı kurulumunu yapar (sadece ilk sefer veya değişiklik olduğunda)"""
    # ChromaDB koleksiyonunu kontrol et
    try:
        from chroma_yonetici import soru_koleksiyonu_getir
        koleksiyon = soru_koleksiyonu_getir()
        if koleksiyon.count() > 0:
            print("✅ ChromaDB'de zaten veri var - yükleme yapılmadı")
            return
    except:
        pass
    
    # Dosya varlık kontrolü
    if not os.path.exists(dosya_yolu):
        print(f"❌ Hata: {dosya_yolu} dosyası bulunamadı!")
        return
    
    # Güncelleme yap
    veritabani_guncelleme_yap(dosya_yolu)

def main():
    print("🚀 ChatBot başlatılıyor...")
    
    # Otomatik güncelleme yap
    print("🔄 Veritabanı kontrol ediliyor...")
    otomatik_kurulum("veri_dosyasi.csv")

    print("\nÇıkmak için 'q'")
    print("Veri setini görmek için 'data'")
    print("Yenilemek için 'refresh'\n")
    
    while True:
        soru = input("Lütfen sorunuzu yazınız: ").strip()
        
        if soru.lower() == "data":
            veritabani_sorulari_listele()
            continue

        if soru.lower() == 'refresh':
            print("🔁 Veritabanı yenileniyor...")
            client.delete_collection(name="soru_cevap")
            veritabani_guncelleme_yap("veri_dosyasi.csv")
            continue

        if soru.lower() == 'q':
            print("👋 Program sonlandırıldı")
            break

        if not soru:
            print("Lütfen geçerli bir soru girin.")
            continue
            
        cevap, en_yakin_soru, benzerlik = soru_cevapla(soru)
        
        print("\n" + "="*50)
        
        # Sadece benzerlik yeterliyse cevabı göster
        if benzerlik >= 75:
            print(f"❓ Sizin Sorunuz: {soru}")
            print(f"🔍 En Yakın Soru: {en_yakin_soru}")
            print(f"🧠 Cevap: {cevap}")
            print(f"📊 Benzerlik Oranı: %{benzerlik}")
        else:
            print("Üzgünüm, yerel veritabanında bu konuda yeterli bilgi yok.")
            print("OpenAI ile araştırıyorum...")            
            # OpenAI'dan cevap al
            openai_cevap = openai_soru_cevapla(soru)
            if openai_cevap:
                print("\n🤖 OpenAI Cevabı:")
                print(openai_cevap)
                soru_ekle(soru, openai_cevap)
            else:
                print("OpenAI'dan cevap alınamadı. Sorunuzu farklı şekilde ifade etmeyi deneyebilir misiniz?")
        
        print("="*50)

if __name__ == "__main__":
    main()