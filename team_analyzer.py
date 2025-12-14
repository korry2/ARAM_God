from lol_library import ChampionLibrary

class TeamAnalyzer:
    def __init__(self):
        self.lib = ChampionLibrary()

    def analyze_team(self, champion_names):
        """Verilen 5 şampiyon ismini analiz eder ve takım raporu çıkarır."""
        
        team_stats = {
            "total_attack": 0,   # Fiziksel Hasar Potansiyeli
            "total_magic": 0,    # Büyü Hasarı Potansiyeli
            "total_defense": 0,  # Dayanıklılık
            "roles": []          # Roller (Mage, Tank vs.)
        }
        
        found_champs = []
        
        print(f"\n--- TAKIM ANALİZİ BAŞLIYOR ---")
        print(f"İncelenen Takım: {', '.join(champion_names)}")
        
        for name in champion_names:
            champ = self.lib.get_champion_stats(name)
            if champ:
                found_champs.append(champ['name'])
                # Riot'un verdiği 1-10 arası puanları topluyoruz
                # Not: Bu veriler 'info' anahtarı altındadır, library'de 'info'yu da çekmemiz lazım.
                # Ancak library şu an sadece 'stats' çekiyor. 
                # O yüzden library'den tam veriyi çekmek için küçük bir hile yapacağız:
                # Doğrudan self.lib.champions içinden ham veriye bakacağız.
                
                # İsim formatlaması (Library'deki mantığın aynısı)
                formatted_name = name.replace(" ", "").replace("'", "").capitalize()
                if formatted_name == "Wukong": formatted_name = "MonkeyKing"
                
                # Ham veriyi bul
                raw_data = None
                if formatted_name in self.lib.champions:
                    raw_data = self.lib.champions[formatted_name]
                else:
                    # İsimle arama
                    for key, val in self.lib.champions.items():
                        if val["name"].lower() == name.lower():
                            raw_data = val
                            break
                
                if raw_data:
                    info = raw_data["info"]
                    team_stats["total_attack"] += info["attack"]
                    team_stats["total_magic"] += info["magic"]
                    team_stats["total_defense"] += info["defense"]
                    team_stats["roles"].extend(raw_data["tags"])

        # --- RAPORLAMA ---
        print("-" * 30)
        print(f"Bulunan Şampiyonlar: {len(found_champs)}/5")
        
        # 1. Hasar Dengesi Analizi
        total_damage_score = team_stats["total_attack"] + team_stats["total_magic"]
        if total_damage_score > 0:
            phys_ratio = (team_stats["total_attack"] / total_damage_score) * 100
            magic_ratio = (team_stats["total_magic"] / total_damage_score) * 100
            
            print(f"\n[HASAR DAĞILIMI]")
            print(f"Fiziksel: %{phys_ratio:.1f}")
            print(f"Büyü    : %{magic_ratio:.1f}")
            
            if phys_ratio > 70:
                print("UYARI: Takım aşırı Fiziksel hasar ağırlıklı! Karşı takım Zırh kasarsa işiniz zor.")
            elif magic_ratio > 70:
                print("UYARI: Takım aşırı Büyü hasarı ağırlıklı! Karşı takım Büyü Direnci kasarsa işiniz zor.")
            else:
                print("ONAY: Hasar dağılımı dengeli. (Hybrid)")

        # 2. Dayanıklılık Analizi
        print(f"\n[DAYANIKLILIK]")
        avg_defense = team_stats["total_defense"] / 5
        print(f"Takım Savunma Puanı: {team_stats['total_defense']} (Ort: {avg_defense:.1f})")
        
        has_tank = "Tank" in team_stats["roles"]
        if not has_tank and avg_defense < 4:
            print("KRİTİK UYARI: Takımda TANK yok ve çok kırılgansınız! (Squishy)")
            print("Öneri: Biriniz fedakarlık yapıp Tank almalı.")
        elif has_tank:
            print("ONAY: Takımda en az bir Tank sınıfı var.")

        # 3. Kitle Kontrol (CC) ve Sınıf Analizi
        # Basitçe rolleri sayalım
        role_counts = {role: team_stats["roles"].count(role) for role in set(team_stats["roles"])}
        print(f"\n[ROL DAĞILIMI]")
        print(role_counts)

# --- TEST ALANI ---
if __name__ == "__main__":
    analyzer = TeamAnalyzer()
    
    # Test Senaryosu 1: Kırılgan, Büyücü ağırlıklı bir takım
    test_team_1 = ["Lux", "Xerath", "Jhin", "Sona", "Teemo"]
    analyzer.analyze_team(test_team_1)
    
    # Test Senaryosu 2: Dengeli bir takım
    print("\n" + "="*40 + "\n")
    test_team_2 = ["Malphite", "Yasuo", "Orianna", "Jinx", "Lulu"]
    analyzer.analyze_team(test_team_2)