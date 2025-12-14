import sys
import time
from team_analyzer import TeamAnalyzer
from smart_advisor import SmartAdvisor
from lcu_connector import LCUConnector
from lol_library import ChampionLibrary

def get_live_champions(connector, lib):
    """Canlı seçim ekranındaki şampiyonları bulur."""
    data = connector.get_champ_select_data()
    if not data:
        return None, None

    my_team = []
    enemy_team = []

    # Bizim Takım (myTeam)
    for player in data.get("myTeam", []):
        champ_id = player.get("championId")
        # ID 0 ise şampiyon seçilmemiştir
        if champ_id and champ_id != 0:
            name = lib.get_champion_by_id(champ_id)
            if name:
                my_team.append(name)

    # Rakip Takım (theirTeam) - ARAM'da bazen görünmeyebilir ama deneyeceğiz
    for player in data.get("theirTeam", []):
        champ_id = player.get("championId")
        if champ_id and champ_id != 0:
            name = lib.get_champion_by_id(champ_id)
            if name:
                enemy_team.append(name)
                
    return my_team, enemy_team

def main():
    print("==================================================")
    print("      ARAM GOD - OTO PİLOT MODU v2.0              ")
    print("==================================================")
    
    # Araçları başlat
    lib = ChampionLibrary()
    analyzer = TeamAnalyzer()
    advisor = SmartAdvisor()
    connector = LCUConnector()
    
    # LoL'e bağlan
    if not connector.connect():
        input("Programı kapatıp LoL'ü açtıktan sonra tekrar dene...")
        sys.exit()

    while True:
        print("\n[MENÜ]")
        print("1. CANLI ANALİZ (Seçim Ekranını Tara)")
        print("2. Manuel Giriş (Eski Usul)")
        print("3. Çıkış")
        
        secim = input("\nSeçim: ")
        
        if secim == "1":
            print("\nSeçim ekranı taranıyor...")
            my_team, enemy_team = get_live_champions(connector, lib)
            
            if my_team:
                print(f"\n✅ TESPİT EDİLEN TAKIM: {', '.join(my_team)}")
                
                if len(my_team) < 5:
                    print("(Henüz herkes şampiyon seçmemiş olabilir)")
                
                # Analiz Yap
                analyzer.analyze_team(my_team)
                
                # Rakip varsa ona da bak
                if enemy_team and len(enemy_team) > 0:
                    print(f"\n✅ TESPİT EDİLEN RAKİPLER: {', '.join(enemy_team)}")
                    advisor.advise(enemy_team)
                else:
                    print("\nℹ️ Rakip takım henüz görünmüyor (veya yükleme ekranına geçilmedi).")
            else:
                print("❌ Şampiyon seçim ekranında değilsin veya veri alınamadı.")
            
            input("\nDevam etmek için Enter...")

        elif secim == "2":
            # Manuel mod (Yedek olarak kalsın)
            print("\nBizimkiler (Virgülle ayır):")
            my_team = [x.strip() for x in input().split(",")]
            analyzer.analyze_team(my_team)
            
            print("\nRakipler (Virgülle ayır):")
            enemy_team = [x.strip() for x in input().split(",")]
            advisor.advise(enemy_team)
            
        elif secim == "3":
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKapatılıyor...")