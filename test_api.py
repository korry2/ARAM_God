import requests
import config

# Türkiye sunucusu (TR1) üzerinden test yapıyoruz
# Bedava şampiyon rotasyonunu sorarak anahtarı deniyoruz
url = f"https://tr1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={config.api_key}"

print("Riot sunucularına bağlanılıyor...")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("\n------------------------------------------------")
    print("BAŞARILI! KAPI AÇILDI.")
    print("------------------------------------------------")
    print(f"Maksimum Yeni Oyuncu Seviyesi: {data['maxNewPlayerLevel']}")
    print(f"Şu an bedava olan şampiyon ID'lerinden ilk 5 tanesi: {data['freeChampionIds'][:5]}")
    print("Sistem tıkır tıkır işliyor Koray.")
elif response.status_code == 403:
    print("\n!!! HATA: ANAHTAR GEÇERSİZ !!!")
    print("API Key yanlış kopyalanmış veya süresi dolmuş olabilir.")
else:
    print("\nBir sorun var.")
    print("Hata Kodu:", response.status_code)