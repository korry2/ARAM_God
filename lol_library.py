import json
import os

class ChampionLibrary:
    def __init__(self):
        self.champions = {}
        self.items = {}
        self.load_data()

    def load_data(self):
        """İndirilmiş JSON dosyalarını hafızaya yükler."""
        try:
            # Şampiyonları yükle
            with open("data/champion.json", "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                # Riot veriyi "data" anahtarı altında tutar, orayı alıyoruz
                self.champions = raw_data["data"]
            
            # Eşyaları yükle
            with open("data/item.json", "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self.items = raw_data["data"]
                
            print(f"Kütüphane Hazır: {len(self.champions)} şampiyon ve {len(self.items)} eşya yüklendi.")
            
        except FileNotFoundError:
            print("HATA: Veri dosyaları bulunamadı! Önce data_manager.py'yi çalıştır.")

    def get_champion_stats(self, champion_name):
        """İsmi verilen şampiyonun temel özelliklerini ve sınıfını döndürür."""
        # Riot verisinde şampiyon isimleri boşluksuz ve büyük harfle başlar (Örn: LeeSin, DrMundo)
        # Bu yüzden basit bir düzeltme yapıyoruz (Spacesiz hale getiriyoruz)
        formatted_name = champion_name.replace(" ", "").replace("'", "").capitalize()
        
        # Bazı özel durumlar için manuel düzeltme (Wukong -> MonkeyKing gibi)
        if formatted_name == "Wukong": formatted_name = "MonkeyKing"

        # Şampiyonu sözlükte ara
        # Not: Tam eşleşme arıyoruz, bulamazsak döngüyle arayacağız
        champ_data = self.champions.get(formatted_name)

        if not champ_data:
            # Eğer direkt bulamazsak, tüm listeyi tarayıp isme benzeyen var mı bakalım
            for key, val in self.champions.items():
                if val["name"].lower() == champion_name.lower():
                    champ_data = val
                    break
        
        if champ_data:
            return {
                "name": champ_data["name"],
                "title": champ_data["title"],
                "tags": champ_data["tags"], # Sınıfları (Mage, Tank vs.)
                "stats": champ_data["stats"] # Can, Zırh, Saldırı Gücü vb.
            }
        else:
            return None
        
    def get_champion_by_id(self, champ_id):
        """Verilen ID numarasının (örn: 222) hangi şampiyon olduğunu bulur."""
        # ID string gelebilir, integer'a çevirelim
        try:
            champ_id = int(champ_id)
        except:
            return None

        for key, val in self.champions.items():
            if int(val["key"]) == champ_id:
                return val["name"]
        return None

# --- TEST ALANI ---
# Bu dosya doğrudan çalıştırıldığında burası devreye girer.
if __name__ == "__main__":
    lib = ChampionLibrary()
    
    # Test: Rastgele bir şampiyon soralım
    test_champ = "Ahri"
    info = lib.get_champion_stats(test_champ)
    
    if info:
        print(f"\n--- {info['name']} ({info['title']}) ---")
        print(f"Sınıflar: {info['tags']}")
        print(f"Başlangıç Canı: {info['stats']['hp']}")
        print(f"Başlangıç Saldırı Gücü: {info['stats']['attackdamage']}")
        print(f"Zırh: {info['stats']['armor']}")
    else:
        print(f"{test_champ} bulunamadı.")