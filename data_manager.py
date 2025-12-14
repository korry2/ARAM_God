import requests
import json
import os

def get_latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()[0]
    except Exception as e:
        print(f"Sürüm hatası: {e}")
    return None

def download_data(version):
    if not os.path.exists("data"):
        os.makedirs("data")

    # Hem Türkçe hem İngilizce rünleri indiriyoruz
    files_to_download = {
        "champion": f"http://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/champion.json",
        "item": f"http://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/item.json",
        "runesReforged_TR": f"http://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/runesReforged.json",
        "runesReforged_EN": f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
    }

    print(f"--- {version} Sürümü İçin Veriler İndiriliyor ---")

    for key, url in files_to_download.items():
        print(f"{key} indiriliyor...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"data/{key}.json", "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
                print(f"TAMAM: {key}.json")
            else:
                print(f"HATA: {key} indirilemedi.")
        except Exception as e:
            print(f"HATA: {e}")

    print("\n--- GÜNCELLEME TAMAMLANDI ---")

if __name__ == "__main__":
    ver = get_latest_version()
    if ver:
        download_data(ver)