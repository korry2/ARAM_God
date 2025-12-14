import psutil
import base64
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_diagnosis():
    print("--- ARAM GOD TANI MERKEZİ ---")
    
    # 1. BAĞLANTIYI BUL
    auth_token = None
    port = None
    
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['name'] == "LeagueClientUx.exe":
            for arg in proc.info['cmdline']:
                if arg.startswith('--remoting-auth-token='):
                    auth_token = arg.split('=')[1]
                elif arg.startswith('--app-port='):
                    port = arg.split('=')[1]
            break
            
    if not port:
        print("❌ HATA: LoL İstemcisi (LeagueClientUx.exe) bulunamadı!")
        print("ÇÖZÜM: Oyunu açtığından emin ol.")
        return

    print(f"✅ BAĞLANTI: Port {port} bulundu.")
    
    base_url = f"https://127.0.0.1:{port}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'riot:{auth_token}'.encode()).decode()}",
        "Accept": "application/json"
    }

    # 2. ŞAMPİYON SEÇİM EKRANI KONTROLÜ
    print("\n--- TEST 1: Şampiyon Seçim Ekranı ---")
    url_champ = f"{base_url}/lol-champ-select/v1/session"
    try:
        resp = requests.get(url_champ, headers=headers, verify=False)
        print(f"Durum Kodu: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print("✅ SONUÇ: Veri Geliyor!")
            print(f"Oyun Modu: {data.get('gameMode', 'Bilinmiyor')}")
            print(f"Bizim Takım Sayısı: {len(data.get('myTeam', []))}")
            # Ham verinin başını gösterelim
            print("Ham Veri (İlk 200 karakter):")
            print(str(data)[:200])
        elif resp.status_code == 404:
            print("❌ SONUÇ: 404 Bulunamadı.")
            print("ANLAMI: Şu an şampiyon seçim ekranında değilsin.")
            print("ÇÖZÜM: Özel oyunu kurdun ama 'Oyunu Başlat'a basıp karakter seçme ekranına girmedin.")
        else:
            print(f"⚠️ SONUÇ: Beklenmedik kod ({resp.status_code})")
            
    except Exception as e:
        print(f"HATA: {e}")

    # 3. LOBİ KONTROLÜ
    print("\n--- TEST 2: Lobi Kontrolü ---")
    url_lobby = f"{base_url}/lol-lobby/v2/lobby"
    try:
        resp = requests.get(url_lobby, headers=headers, verify=False)
        if resp.status_code == 200:
            print("ℹ️ BİLGİ: Şu an Lobidesin (Arkadaş davet etme ekranı).")
            print("Lütfen 'Oyunu Başlat' butonuna bas.")
        else:
            print("ℹ️ BİLGİ: Lobide değilsin.")
    except:
        pass

if __name__ == "__main__":
    run_diagnosis()
    input("\nKapatmak için Enter'a bas...")