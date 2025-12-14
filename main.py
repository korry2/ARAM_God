import sys
from team_analyzer import TeamAnalyzer
from smart_advisor import SmartAdvisor

def main():
    print("==================================================")
    print("          ARAM GOD - SAVAŞ ASİSTANI v1.1          ")
    print("==================================================")
    
    analyzer = TeamAnalyzer()
    advisor = SmartAdvisor()
    
    while True:
        print("\n[MENÜ]")
        print("1. Tam Maç Analizi (Bizim Takım vs Rakip Takım)")
        print("2. Çıkış")
        
        secim = input("\nSeçimin nedir (1-2): ")
        
        if secim == "1":
            # 1. BİZİM TAKIM
            print("\n--- ADIM 1: BİZİM TAKIM ---")
            print("Takımındaki şampiyonları virgülle ayırarak yaz.")
            my_team_input = input("Bizimkiler: ")
            my_team = [x.strip() for x in my_team_input.split(",")]
            
            if len(my_team) < 5:
                print("Bilgi: Eksik şampiyon girdin ama devam ediyorum.")

            # Bizim takımın analizi
            analyzer.analyze_team(my_team)
            
            # 2. RAKİP TAKIM
            print("\n--- ADIM 2: RAKİP TAKIM ---")
            print("Rakip şampiyonları virgülle ayırarak yaz.")
            enemy_team_input = input("Rakipler: ")
            enemy_team = [x.strip() for x in enemy_team_input.split(",")]
            
            # Danışman devreye giriyor
            advisor.advise(enemy_team)
            
            input("\nAna menüye dönmek için Enter'a bas...")
            
        elif secim == "2":
            print("Görüşmek üzere Koray. İyi oyunlar!")
            sys.exit()
        else:
            print("Geçersiz seçim. Tekrar dene.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram kapatıldı.")