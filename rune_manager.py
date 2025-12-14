import requests
from bs4 import BeautifulSoup
from lol_library import ChampionLibrary

class RuneManager:
    def __init__(self, connector):
        self.connector = connector
        self.lib = ChampionLibrary()
        self.base_url = "https://www.aramonly.com/guide"
        # Tarayıcı taklidi yapmak için başlık
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    def get_runes_from_url(self, url):
        """Verilen URL'den rünleri çekmeye çalışır."""
        print(f"   -> Bağlanılıyor: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code != 200:
                print(f"   ⚠️ Sayfa açılamadı (Kod: {response.status_code})")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            found_runes = []
            
            # Yöntem 1: Resimlerin 'alt' etiketlerinden bul
            for img in soup.find_all('img'):
                alt_text = img.get('alt')
                if alt_text:
                    rune_id = self.lib.get_rune_id(alt_text)
                    if rune_id:
                        found_runes.append(rune_id)
            
            # Listeyi temizle
            unique_runes = list(dict.fromkeys(found_runes))
            
            if len(unique_runes) >= 6:
                return unique_runes
            else:
                return None

        except Exception as e:
            print(f"   ⚠️ Hata: {e}")
            return None

    def decide_and_apply(self, champion_name, team_analysis):
        """Takım durumuna göre en iyi buildi seçer, indirir ve uygular."""
        
        print(f"\n--- {champion_name.upper()} İÇİN RÜN OPERASYONU ---")
        
        # URL için isim formatı (Dr. Mundo -> dr-mundo)
        url_name = champion_name.lower().replace(".", "").replace(" ", "-").replace("'", "")
        
        # 1. PLAN A: Özel Build Dene
        target_variant = ""
        reason = "Dengeli"
        
        if "Tank" not in team_analysis["roles"] and team_analysis["avg_defense"] < 4:
            target_variant = "/tank-build"
            reason = "Takımda Tank Yok -> Tank Build deneniyor"
        elif team_analysis["magic_ratio"] < 20:
            target_variant = "/ap-build"
            reason = "Takımda AP Yok -> AP Build deneniyor"
            
        print(f"Strateji: {reason}")
        
        rune_ids = None
        
        # Eğer özel bir build gerekiyorsa önce onu dene
        if target_variant:
            target_url = f"{self.base_url}/{url_name}{target_variant}"
            rune_ids = self.get_runes_from_url(target_url)
        
        # 2. PLAN B: Eğer Plan A tutmazsa (veya gerekmezse), Varsayılan Build'e dön
        if not rune_ids:
            if target_variant:
                print("   ⚠️ Özel build bulunamadı veya hatalı. Varsayılan build'e geçiliyor...")
            
            default_url = f"{self.base_url}/{url_name}"
            rune_ids = self.get_runes_from_url(default_url)
            
        # 3. SONUÇ
        if rune_ids:
            print(f"✅ Rünler Bulundu: {rune_ids[:6]}...")
            self.push_runes_to_client(champion_name, rune_ids)
        else:
            print("❌ HATA: Hiçbir kaynaktan rün verisi çekilemedi.")

    def push_runes_to_client(self, page_name, rune_ids):
        """Rünleri LoL istemcisine kaydeder."""
        if not self.connector.base_url:
            print("LoL bağlantısı yok, rünler ayarlanamadı.")
            return

        # Mevcut sayfayı sil
        try:
            current_page = requests.get(
                f"{self.connector.base_url}/lol-perks/v1/currentpage",
                headers=self.connector.headers,
                verify=False
            ).json()
            
            if 'id' in current_page:
                requests.delete(
                    f"{self.connector.base_url}/lol-perks/v1/pages/{current_page['id']}",
                    headers=self.connector.headers,
                    verify=False
                )
        except:
            pass # Hata olursa devam et, belki sayfa yoktur

        # Yeni Sayfa
        # 8000 (Precision), 8100 (Domination), 8200 (Sorcery), 8300 (Inspiration), 8400 (Resolve)
        # Basitlik için varsayılan 8000/8100 gönderiyoruz, rün ID'leri doğruysa LoL bunu otomatik düzeltir.
        new_page_data = {
            "name": f"ARAM GOD: {page_name}",
            "primaryStyleId": 8000, 
            "subStyleId": 8100,
            "selectedPerkIds": rune_ids[:9],
            "current": True
        }
        
        resp = requests.post(
            f"{self.connector.base_url}/lol-perks/v1/pages",
            headers=self.connector.headers,
            json=new_page_data,
            verify=False
        )
        
        if resp.status_code == 200:
            print("✅ BAŞARILI: Rünler LoL'e yüklendi ve seçildi!")
        else:
            print(f"Rün yükleme hatası: {resp.text}")