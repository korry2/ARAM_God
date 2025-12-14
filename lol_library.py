import json
import os

class ChampionLibrary:
    def __init__(self):
        self.champions = {}
        self.items = {}
        self.runes = {} 
        self.load_data()

    def load_data(self):
        try:
            # Şampiyonlar ve Eşyalar
            with open("data/champion.json", "r", encoding="utf-8") as f:
                self.champions = json.load(f)["data"]
            with open("data/item.json", "r", encoding="utf-8") as f:
                self.items = json.load(f)["data"]

            # Rün Yükleme Fonksiyonu (Tekrarı önlemek için)
            def load_rune_file(filename):
                if os.path.exists(filename):
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for tree in data:
                            # Ağaç isimleri (Domination / Hakimiyet)
                            self.runes[tree["name"]] = tree["id"]
                            self.runes[tree["key"]] = tree["id"]
                            # Rünler
                            for slot in tree["slots"]:
                                for rune in slot["runes"]:
                                    self.runes[rune["name"]] = rune["id"]
                                    self.runes[rune["key"]] = rune["id"]

            # Hem TR hem EN dosyalarını yükle
            load_rune_file("data/runesReforged_TR.json")
            load_rune_file("data/runesReforged_EN.json")
            
            print(f"Kütüphane Hazır: {len(self.champions)} şampiyon, {len(self.items)} eşya ve Çift Dilli Rünler.")
            
        except FileNotFoundError:
            print("HATA: Veri dosyaları eksik. data_manager.py çalıştır.")

    def get_champion_stats(self, champion_name):
        formatted_name = champion_name.replace(" ", "").replace("'", "").capitalize()
        if formatted_name == "Wukong": formatted_name = "MonkeyKing"
        
        if formatted_name in self.champions:
            return self.champions[formatted_name]
        
        for key, val in self.champions.items():
            if val["name"].lower() == champion_name.lower():
                return val
        return None

    def get_champion_by_id(self, champ_id):
        try:
            champ_id = int(champ_id)
        except:
            return None
        for key, val in self.champions.items():
            if int(val["key"]) == champ_id:
                return val["name"]
        return None

    def get_rune_id(self, text):
        """Metin içindeki rün ismini bulur (Örn: 'Major rune Aftershock...' -> 8439)"""
        if not text: return None
        
        # 1. Tam Eşleşme Kontrolü
        if text in self.runes:
            return self.runes[text]
            
        # 2. Cümle İçinde Arama (Fuzzy Search)
        # En uzun isimden en kısaya doğru arayalım ki 'Ice' yerine 'Iceborn'u bulsun.
        sorted_runes = sorted(self.runes.keys(), key=len, reverse=True)
        
        text_lower = text.lower()
        
        for rune_name in sorted_runes:
            # Rün ismi cümle içinde geçiyor mu?
            if rune_name.lower() in text_lower:
                return self.runes[rune_name]
                
        return None