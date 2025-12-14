import sys
import time
from team_analyzer import TeamAnalyzer
from smart_advisor import SmartAdvisor
from lcu_connector import LCUConnector
from lol_library import ChampionLibrary
from rune_manager import RuneManager

def get_live_champions(connector, lib):
    data = connector.get_champ_select_data()
    if not data: return None, None, None
    
    my_team = []
    enemy_team = []
    my_champion = None
    
    # Kendi hücre ID'mizi bulalım
    local_cell_id = data.get("localPlayerCellId")
    
    # Bizim Takım
    for player in data.get("myTeam", []):
        champ_id = player.get("championId")
        # ID 0 ise şampiyon seçilmemiştir, atla
        if champ_id and champ_id != 0:
            name = lib.get_champion_by_id(champ_id)
            if name:
                my_team.append(name)
                # Eğer bu oyuncu bizsek, şampiyonumuzu kaydet
                if player.get("cellId") == local_cell_id:
                    my_champion = name

    # Rakip Takım
    for player in data.get("theirTeam", []):
        champ_id = player.get("championId")
        if champ_id and champ_id != 0:
            name = lib.get_champion_by_id(champ_id)
            if name:
                enemy_team.append(name)
                
    return my_team, enemy_team, my_champion

def main():
    print("==================================================")
    print("      ARAM GOD - TANRI MODU (PUSU MODU)           ")
    print("==================================================")
    
    lib = ChampionLibrary()
    analyzer = TeamAnalyzer()
    advisor = SmartAdvisor()
    connector = LCUConnector()
    
    if not connector.connect():
        print("LoL açık değil. Lütfen oyunu aç.")
        input("Çıkış için Enter...")
        sys.exit()

    rune_manager = RuneManager(connector)

    while True:
        print("\n[MENÜ]")
        print("1. OTO PİLOTU BAŞLAT (Seçim Yapmanı Bekler)")
        print("2. Çıkış")
        
        secim = input("\nSeçim: ")
        
        if secim == "1":
            print("\n⏳ Pusuya yatıldı... Şampiyon seçmen bekleniyor...")
            print("(Yasaklama ekranındaysan veya henüz seçmediysen bekle, program takipte.)")
            
            # PUSU DÖNGÜSÜ
            last_champ = None
            while True:
                try:
                    my_team, enemy_team, my_champ = get_live_champions(connector, lib)
                    
                    # Eğer veri gelmiyorsa (Seçimden çıktıysan)
                    if my_team is None:
                        print("❌ Seçim ekranından çıkıldı. Menüye dönülüyor.")
                        break

                    # Eğer bir şampiyon seçtiysen ve bu yeni bir seçimse
                    if my_champ and my_champ != last_champ:
                        print(f"\n⚡ TESPİT EDİLDİ: {my_champ}")
                        last_champ = my_champ
                        
                        # 1. Takım Analizi
                        print("--- Takım Analizi ---")
                        analyzer.analyze_team(my_team)
                        
                        # 2. Rünleri Ayarla
                        print("\n--- Rün Operasyonu ---")
                        # Basit istatistik çıkarma
                        total_magic = 0
                        total_defense = 0
                        roles = []
                        for name in my_team:
                            c = lib.get_champion_stats(name)
                            if c:
                                total_magic += c["info"]["magic"]
                                total_defense += c["info"]["defense"]
                                roles.extend(c["tags"])
                        
                        team_stats = {
                            "avg_defense": total_defense / 5 if len(my_team) > 0 else 0,
                            "magic_ratio": (total_magic / (total_magic + 1)) * 100,
                            "roles": roles
                        }
                        
                        rune_manager.decide_and_apply(my_champ, team_stats)
                        
                        # 3. Rakip Analizi (Varsa)
                        if enemy_team:
                            advisor.advise(enemy_team)
                        
                        print("\n✅ İŞLEM TAMAM. Başka bir şampiyona geçersen otomatik güncellerim.")
                        print("Çıkmak için CTRL+C yapabilirsin veya oyun başlayınca kapanır.")

                    # Her 2 saniyede bir kontrol et
                    time.sleep(2)
                    
                except KeyboardInterrupt:
                    print("\nMenüye dönülüyor...")
                    break
                except Exception as e:
                    print(f"Hata oluştu: {e}")
                    time.sleep(2)

        elif secim == "2":
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKapatılıyor...")