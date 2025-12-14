import requests
import json
import os

def get_latest_version():
    """Riot sunucularından en son LoL yama sürümünü (örn: 14.23.1) öğrenir."""
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            versions = response.json()
            return versions[0] # Listenin ilk elemanı en güncel sürümdür
    except Exception as e:
        print(f"Sürüm kontrolünde hata: {e}")
    return None

def download_data(version):
    """Verilen sürüme ait şampiyon ve eşya verilerini indirip kaydeder."""
    
    # Verileri kaydedeceğimiz 'data' klasörünü oluştur (yoksa)
    if not os.path.exists("data"):
        os.makedirs("data")
        print("'data' klasörü oluşturuldu.")

    # İndirilecek dosyaların listesi (URL tipi ve Dosya adı)
    files_to_download = {
        "champion": f"http://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/champion.json",
        "item": f"http://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/item.json"
    }

    print(f"--- {version} Sürümü İçin Veriler İndiriliyor ---")

    for key, url in files_to_download.items():
        print(f"{key} verisi indiriliyor...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Dosyayı bilgisayara kaydet
                file_path = f"data/{key}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
                print(f"TAMAM: {file_path} başarıyla kaydedildi.")
            else:
                print(f"HATA: {key} indirilemedi. Kod: {response.status_code}")
        except Exception as e:
            print(f"HATA: {key} indirilirken bir sorun oluştu: {e}")

    print("\n--- TÜM İNDİRMELER TAMAMLANDI ---")

if __name__ == "__main__":
    latest_version = get_latest_version()
    if latest_version:
        print(f"Tespit edilen en güncel sürüm: {latest_version}")
        download_data(latest_version)
    else:
        print("Güncel sürüm bilgisi alınamadı. İnternet bağlantını kontrol et.")