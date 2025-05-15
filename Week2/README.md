# Teknik Soru-Cevap ChatBotu 🤖

Bu proje, yazılım, yapay zeka, programlama ve siber güvenlik gibi teknik konularda kullanıcıların sorularına yanıt veren bir ChatBot sistemidir. Sistem öncelikle ChromaDB üzerinde embed edilmiş veri kümesi üzerinden cevap arar, yeterli benzerlik bulunamazsa OpenAI API'yi kullanarak yanıt üretir ve yeni soruları veritabanına kaydeder.

## 🚀 Özellikler

- Embedding tabanlı benzerlik karşılaştırması (SentenceTransformer)
- ChromaDB ile lokal vektör veritabanı
- OpenAI GPT API ile desteklenen ikinci seviye yanıt sistemi
- Sadece teknik sorulara cevap verir
- Soru-cevap veri seti CSV formatında dışarıdan güncellenebilir

## 📁 Dosya Yapısı

- `chat_bot.py` - Ana uygulama dosyası
- `chroma_yonetici.py` - Embedding ve ChromaDB işlemleri
- `veritabani_yonetici.py` - CSV'den veritabanı güncelleme ve yönetimi
- `veri_dosyasi.csv` - Başlangıç veri kümesi (question-answer)
- `openai.env` - OpenAI API anahtarı (örnek: `OPENAI_API_KEY=...`)

## 🧪 Kullanım

```bash
# 1️⃣ ChromaDB sunucusunu başlat (ayrı bir terminalde çalıştır)
chroma run --path /path/to/data

# 2️⃣ Ana uygulamayı çalıştır
python chat_bot.py
```
## Komutlar:

q    : Programı sonlandır
data : Kayıtlı veri setini göster
refresh : CSV dosyasındaki verilerle ChromaDB'yi yeniden yükle

## ⚙️ Gereksinimler
Gerekli Python paketleri için requirements.txt dosyasını kullanın.

## 📌 Notlar
- ChromaDB servisinin localhost:8000 üzerinde çalışıyor olması gerekir.
- 'chroma run' komutu, internet bağlantısına ihtiyaç duymadan lokal olarak vektör veritabanını başlatır. Uygulamanın doğru çalışması için bu servis arka planda açık olmalıdır.
- veri_dosyasi.csv içinde question ve answer sütunları bulunmalıdır.
- OpenAI yanıtları da ChromaDB'ye eklenerek sistemin zamanla kendini geliştirmesi sağlanır.