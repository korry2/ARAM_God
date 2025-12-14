import psutil
import base64
import requests
import urllib3
import json

# Güvenlik sertifikası uyarılarını sustur (LoL yerel sunucusu sertifikasızdır)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LCUConnector:
    def __init__(self):
        self.process_name = "LeagueClientUx.exe"
        self.port = None
        self.auth_token = None
        self.headers = {}
        self.base_url = ""

    def connect(self):
        """Çalışan LoL istemcisini bulur ve bağlantı bilgilerini çeker."""
        print("LoL İstemcisi aranıyor...")
        
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                if proc.info['name'] == self.process_name:
                    args = proc.info['cmdline']
                    
                    # Şifre ve Port bilgilerini argümanlardan ayıkla
                    for arg in args:
                        if arg.startswith('--remoting-auth-token='):
                            self.auth_token = arg.split('=')[1]
                        elif arg.startswith('--app-port='):
                            self.port = arg.split('=')[1]
                    
                    if self.auth_token and self.port:
                        # Bağlantı URL'sini ve Başlıkları hazırla
                        self.base_url = f"https://127.0.0.1:{self.port}"
                        auth_str = f"riot:{self.auth_token}"
                        auth_b64 = base64.b64encode(auth_str.encode()).decode()
                        
                        self.headers = {
                            "Authorization": f"Basic {auth_b64}",
                            "Accept": "application/json"
                        }
                        print(f"BAĞLANDI: Port {self.port} üzerinden iletişim kuruldu.")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        print("HATA: LoL İstemcisi bulunamadı. Oyunun açık olduğundan emin ol.")
        return False

    def get_champ_select_data(self):
        """Şampiyon seçim ekranındaki verileri çeker."""
        if not self.base_url:
            return None
            
        url = f"{self.base_url}/lol-champ-select/v1/session"
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            if response.status_code == 200:
                return response.json()
            else:
                # Eğer 404 dönerse, şampiyon seçim ekranında değilsin demektir.
                return None
        except:
            return None

# --- TEST ALANI ---
if __name__ == "__main__":
    connector = LCUConnector()
    if connector.connect():
        print("\nVeri çekiliyor...")
        data = connector.get_champ_select_data()
        if data:
            print("Şampiyon Seçim Ekranı Aktif!")
            # Ham veriyi görelim (Test amaçlı)
            print(json.dumps(data, indent=4)[:500] + "...") 
        else:
            print("Şu an şampiyon seçim ekranında değilsin.")