from team_analyzer import TeamAnalyzer

class SmartAdvisor:
    def __init__(self):
        self.analyzer = TeamAnalyzer()
        
        # Kritik Eşya Önerileri Veritabanı
        self.counter_items = {
            "anti_tank_ad": "Dominik Efendi'nin Hürmetleri (LDR)",
            "anti_tank_ap": "Hiçlik Değneği (Void Staff)",
            "anti_heal_ad": "Celladın Çağrısı (Executioner's Calling)",
            "anti_heal_ap": "Morellonomikon",
            "anti_burst": "Sterak'ın Güvencesi / Zhonya",
            "mr_item": "Doğanın Kudreti (Force of Nature)",
            "armor_item": "Çivili Zırh (Thornmail)"
        }

        # İyileştirme yapan belalı şampiyonlar listesi
        self.healers = ["Soraka", "Yuumi", "Sona", "Nami", "Milio", "Vladimir", "Mundo", "Aatrox", "Swain", "Sylas"]

    def advise(self, enemy_champion_names):
        """Karşı takıma bakarak stratejik öneriler sunar."""
        
        print(f"\n--- SAVAŞ DANIŞMANI DEVREDE ---")
        
        # 1. Önce karşı takımı analiz edelim (Bizim yazdığımız analyzer'ı kullanıyoruz)
        # Ancak analyzer ekrana yazdırıyor, biz verileri arka planda istiyoruz.
        # Bu yüzden analyzer kodunu biraz 'hack'leyerek verileri manuel çekeceğiz.
        
        enemy_stats = {
            "total_defense": 0,
            "total_attack": 0,
            "total_magic": 0,
            "roles": [],
            "names": []
        }
        
        healer_count = 0
        
        for name in enemy_champion_names:
            champ = self.analyzer.lib.get_champion_stats(name)
            if champ:
                # İsim düzeltme ve veri çekme (TeamAnalyzer mantığıyla aynı)
                formatted_name = name.replace(" ", "").replace("'", "").capitalize()
                if formatted_name == "Wukong": formatted_name = "MonkeyKing"
                
                raw_data = None
                if formatted_name in self.analyzer.lib.champions:
                    raw_data = self.analyzer.lib.champions[formatted_name]
                else:
                    for key, val in self.analyzer.lib.champions.items():
                        if val["name"].lower() == name.lower():
                            raw_data = val
                            break
                
                if raw_data:
                    info = raw_data["info"]
                    enemy_stats["total_defense"] += info["defense"]
                    enemy_stats["total_attack"] += info["attack"]
                    enemy_stats["total_magic"] += info["magic"]
                    enemy_stats["names"].append(raw_data["name"])
                    
                    # Healer kontrolü
                    if raw_data["name"] in self.healers:
                        healer_count += 1

        # --- STRATEJİ RAPORU ---
        suggestions = []
        
        # 1. Tank Tehdidi Analizi
        avg_defense = enemy_stats["total_defense"] / 5
        if avg_defense >= 5.5:
            print(f"⚠️ DİKKAT: Karşı takım ÇOK DAYANIKLI (Ort. Savunma: {avg_defense:.1f})")
            suggestions.append(f"- AD isen: {self.counter_items['anti_tank_ad']} ALMALISIN.")
            suggestions.append(f"- AP isen: {self.counter_items['anti_tank_ap']} ALMALISIN.")
        else:
            print(f"✅ BİLGİ: Karşı takım kırılgan. Zırh Deşme (Lethality) veya Büyü Nüfuzu etkili olur.")

        # 2. İyileştirme Tehdidi
        if healer_count > 0:
            print(f"⚠️ DİKKAT: Karşıda {healer_count} tane iyileştirici/yenileyici var!")
            suggestions.append(f"- ACİL: {self.counter_items['anti_heal_ad']} veya {self.counter_items['anti_heal_ap']} al.")
        
        # 3. Hasar Türüne Göre Savunma Önerisi
        total_dmg = enemy_stats["total_attack"] + enemy_stats["total_magic"]
        if total_dmg > 0:
            magic_ratio = (enemy_stats["total_magic"] / total_dmg) * 100
            if magic_ratio > 65:
                print("⚠️ DİKKAT: Karşı taraf BÜYÜ hasarı ağırlıklı.")
                suggestions.append(f"- Tank/Dövüşçü isen: {self.counter_items['mr_item']} hayat kurtarır.")
            elif magic_ratio < 35:
                print("⚠️ DİKKAT: Karşı taraf FİZİKSEL hasar ağırlıklı.")
                suggestions.append(f"- Tank/Dövüşçü isen: {self.counter_items['armor_item']} al.")

        # Önerileri Listele
        print("\n[ÖNERİLEN EŞYALAR]")
        if suggestions:
            for s in suggestions:
                print(s)
        else:
            print("- Özel bir counter eşyasına gerek yok. Kendi buildine odaklan.")

# --- TEST ALANI ---
if __name__ == "__main__":
    advisor = SmartAdvisor()
    # Test: Karşıda Dr. Mundo ve Soraka olan tank bir takım olsun
    enemy_team = ["Dr. Mundo", "Soraka", "Rammus", "Vayne", "Lulu"]
    advisor.advise(enemy_team)