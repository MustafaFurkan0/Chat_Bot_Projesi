# Teknik Soru-Cevap ChatBotu 🤖

Bu proje, yazılım, yapay zeka, programlama ve siber güvenlik gibi teknik konularda kullanıcıların sorularına yanıt veren bir ChatBot sistemidir. Sistem öncelikle ChromaDB üzerinde embed edilmiş veri kümesi üzerinden cevap arar, yeterli benzerlik bulunamazsa OpenAI API'yi kullanarak yanıt üretir ve yeni soruları veritabanına kaydeder.

## 🚀 Özellikler

- 📚 **Embedding tabanlı yerel bilgi sorgulama**
- 🤖 **OpenAI GPT-3.5-Turbo entegrasyonu**
- 🧠 **Teknik soru tespiti (kategorilere göre)**
- 🔁 **Yinelenen soru yanıtı yönetimi**
- 🧾 **Şikayet kaydı ve loglama**
- 🌐 **Landbot ile entegrasyon**
- 🛠️ **Otomatik veritabanı kurulumu**


## 📁 Dosya Yapısı

├── main.py            => FastAPI uygulaması ve başlangıç noktası
├── chat_bot.py        => Soru işleme, embedding, OpenAI ve kurulum fonksiyonları
├── chroma_yonetici.py => ChromaDB işlemleri (embedding, ekleme, sorgulama)
├── routers/
│ ├── landbot.py => Landbot API entegrasyonu
│ └── admin.py   => Şikayet kaydı ve log yönetimi
├── utils/
│ └── logger.py  => Global logger ayarları
├── veri_dosyasi.csv      => Başlangıç bilgi kaynağı
├── sikayet_kayitlari.csv => Şikayetlerin tutulduğu CSV
└── openai.env            => OpenAI API anahtarı (çevre değişkeni)

## 🧪 Kullanım

```bash
# 1️⃣ ChromaDB sunucusunu başlat (ayrı bir terminalde çalıştır)
chroma run --path /path/to/data

# 2️⃣ Ana uygulamayı çalıştır
python chat_bot.py
```
## 🧪 Konsol Modu
Proje, terminal üzerinden test edilebilir:
```bash
python chat_bot.py
Komutlar:
q → Çıkış
data → Tüm soruları listeler
refresh → Veritabanını sıfırlar ve CSV’den yeniden yükler
```
## 🚀 Uygulamayı Başlat
``` bash
uvicorn main:app --reload
```
## 🌐 API Endpoint'leri
``` bash
Genel
GET / → Sağlık kontrolü (health check)

Landbot Entegrasyonu
POST /api/landbot/interactive
Landbot’tan gelen etkileşimleri yönetir.
current_step alanına göre cevap üretir.

Admin Paneli
POST /api/admin/log
Kullanıcı şikayetlerini sikayet_kayitlari.csv dosyasına loglar.
```

## ⚙️ Gereksinimler
Gerekli Python paketleri için requirements.txt dosyasını kullanın.

## 📌 Notlar
- ChromaDB servisinin localhost:8001 üzerinde çalışıyor olması gerekir.
- 'chroma run' komutu, internet bağlantısına ihtiyaç duymadan lokal olarak vektör veritabanını başlatır. Uygulamanın doğru çalışması için bu servis arka planda açık olmalıdır.
- OpenAI yanıtları da ChromaDB'ye eklenerek sistemin zamanla kendini geliştirmesi sağlanır.
