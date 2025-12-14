import sys
from team_analyzer import TeamAnalyzer
from stat_calculator import StatCalculator

def main():
    print("==================================================")
    print("          ARAM GOD - SAVAŞ ASİSTANI v1.0          ")
    print("==================================================")
    
    # Araçları hazırlıyoruz
    analyzer = TeamAnalyzer()
    # StatCalculator'ı şimdilik bekletiyoruz, ileride buraya ekleyeceğiz.
    
    while True:
        print("\n[MENÜ]")
        print("1. Takım Analizi Yap (Şampiyon Seçim Ekranı)")
        print("2. Çıkış")
        
        secim = input("\nSeçimin nedir (1-2): ")
        
        if secim == "1":
            print("\nTakımdaki 5 şampiyonun ismini aralarına virgül koyarak yaz.")
            print("Örnek: Malphite, Yasuo, Lulu, Jinx, Zed")
            user_input = input("Şampiyonlar: ")
            
            # Girilen metni virgülden bölüp temizliyoruz
            champ_list = [x.strip() for x in user_input.split(",")]
            
            if len(champ_list) < 5:
                print("UYARI: 5 şampiyon girmedin ama yine de analiz yapıyorum...")
            
            # Analizi başlat
            analyzer.analyze_team(champ_list)
            
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