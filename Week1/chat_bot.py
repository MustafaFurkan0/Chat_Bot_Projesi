import torch
from sentence_transformers import SentenceTransformer
import torch.nn.functional as F
import pandas as pd

# Model yükleniyor
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# CSV'den veri okuma
csv_path = "C:/Users/user/Desktop/Acunmedya-ChatBot_Proje/Week1/siber_guvenlik_sorular.csv"
df = pd.read_csv(csv_path)

# Satırları liste haline getir
data = df.to_dict(orient="records")

# Soru embedding'lerini önceden hesapla
sorular = [item["soru"] for item in data]
soru_embeddingleri = model.encode(sorular, convert_to_tensor=True)

# Komut satırı arayüzü
print("\n*******************************************************************")
print("\n         SİBER GÜVENLİK ASİSTANI — CSV TABANLI\n")
print("*******************************************************************")
print("Çıkmak için 'çık' yazın.\n")
while True:
    user_input = input("Soru girin: ")

    if user_input.lower() == "çık" or "Çık" or "ÇIK":
        print("Asistan sonlandırıldı.")
        break

    input_embedding = model.encode(user_input, convert_to_tensor=True)
    benzerlik_skorlari = F.cosine_similarity(input_embedding, soru_embeddingleri)
    en_yakin_idx = torch.argmax(benzerlik_skorlari).item()
    skor = benzerlik_skorlari[en_yakin_idx].item()

    if skor < 0.70:
        print("⚠️ Teknik bir soru tespit edilemedi. Daha spesifik bir soru girin.\n")
    else:
        print(f"\n✅ En yakın soru  : {data[en_yakin_idx]['soru']}")
        print(f"📌 Cevap          : {data[en_yakin_idx]['cevap']}")
        print(f"🔍 Benzerlik Skoru: {skor:.2f}\n")
