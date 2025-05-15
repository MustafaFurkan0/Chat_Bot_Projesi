## 🔐 Siber Güvenlik Soru-Cevap Asistanı (CSV Tabanlı)

Bu Python projesi, CSV dosyasından alınan siber güvenlik konulu soru-cevap verileriyle çalışan, gömülü (embedding) tabanlı bir komut satırı asistanıdır. Kullanıcıdan gelen sorular, önceden tanımlanmış sorularla karşılaştırılır ve en benzer cevap kullanıcıya sunulur.

---

## 🚀 Özellikler

- 📄 CSV tabanlı soru-cevap veri kaynağı
- 🤖 SentenceTransformer ile çok dilli anlam eşleştirme
- ⚡ PyTorch ile hızlı benzerlik karşılaştırması
- ✅ En benzer soru ve cevabı gösterme
- ❌ Yetersiz benzerlik varsa uyarı verme
- 🔁 Sürekli çalışan komut satırı arayüzü

---

## 📂 CSV Dosya Yapısı
CSV dosyanız aşağıdaki gibi yapılandırılmalıdır:

soru,cevap
"Firewall nedir?","Firewall, ağı zararlı trafiğe karşı koruyan sistemdir."
"Phishing saldırısı nedir?","Phishing, kullanıcıları kandırarak bilgilerini çalmayı hedefleyen saldırılardır."
...

Dosya yolu kodda şu şekilde ayarlanmalıdır:
csv_path = "C:/Users/user/Desktop/Acunmedya-ChatBot_Proje/Week1/siber_guvenlik_sorular.csv"

## ▶ Kullanım
- Projeyi başlat:

python asistan.py

- Terminalde şunu göreceksiniz:

SİBER GÜVENLİK ASİSTANI — CSV TABANLI
Çıkmak için 'çık' yazın.

- Herhangi bir teknik soru sorun:
Soru girin: Phishing nedir?

- Sistem şu yanıtı verebilir:
✅ En yakın soru  : Phishing saldırısı nedir?
📌 Cevap          : Phishing, kullanıcıları kandırarak bilgilerini çalmayı hedefleyen saldırılardır.
🔍 Benzerlik Skoru: 0.88

## ⚙ Eşik Değeri ve Benzerlik:

- Sistem benzerlik skorunu cosine_similarity ile hesaplar.
- Eğer skor 0.70 altında ise cevap vermez ve daha teknik soru ister.
- Bu eşik değeri şu satırda değiştirilebilir:
    if skor < 0.70:
