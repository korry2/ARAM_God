from lol_library import ChampionLibrary

class StatCalculator:
    def __init__(self):
        self.lib = ChampionLibrary()
        
        # Riot'un garip kodlarını Türkçe'ye çeviren sözlük
        self.stat_map = {
            "FlatPhysicalDamageMod": "Saldırı Gücü (AD)",
            "FlatMagicDamageMod": "Yetenek Gücü (AP)",
            "FlatHPPoolMod": "Can (HP)",
            "FlatArmorMod": "Zırh",
            "FlatSpellBlockMod": "Büyü Direnci (MR)",
            "FlatCritChanceMod": "Kritik Vuruş",
            "FlatMovementSpeedMod": "Hareket Hızı",
            "PercentAttackSpeedMod": "Saldırı Hızı"
        }

    def calculate_build(self, champion_name, item_names):
        """Şampiyonun temel özelliklerine eşyaları ekler ve son durumu gösterir."""
        
        # 1. Şampiyonu Bul
        champ = self.lib.get_champion_stats(champion_name)
        if not champ:
            print(f"HATA: {champion_name} bulunamadı.")
            return

        print(f"\n--- {champ['name'].upper()} İÇİN BUILD HESAPLANIYOR ---")
        
        # Temel İstatistikler (Base Stats)
        current_stats = {
            "Saldırı Gücü (AD)": champ['stats']['attackdamage'],
            "Yetenek Gücü (AP)": 0, # Şampiyonlar 0 AP ile başlar
            "Can (HP)": champ['stats']['hp'],
            "Zırh": champ['stats']['armor'],
            "Büyü Direnci (MR)": champ['stats']['spellblock']
        }

        print(f"Eşyalar: {', '.join(item_names)}")
        
        # 2. Eşyaları Bul ve Ekle
        for item_name in item_names:
            found_item = None
            
            # Eşyayı isminden bulmaya çalış
            for key, val in self.lib.items.items():
                if val["name"] == item_name:
                    found_item = val
                    break
            
            if found_item:
                # Eşyanın özelliklerini (stats) mevcut özelliklere ekle
                stats = found_item.get("stats", {})
                for stat_code, value in stats.items():
                    if stat_code in self.stat_map:
                        readable_name = self.stat_map[stat_code]
                        # Eğer listede varsa ekle, yoksa yeni oluştur
                        if readable_name in current_stats:
                            current_stats[readable_name] += value
                        else:
                            current_stats[readable_name] = value
            else:
                print(f"UYARI: '{item_name}' veritabanında bulunamadı (İsim hatası olabilir).")

        # 3. Sonucu Yazdır
        print("\n[SONUÇ TABLOSU]")
        for stat, value in current_stats.items():
            # Sayıları yuvarla (Örn: 76.5 -> 76.5, 76.0 -> 76)
            print(f"{stat}: {round(value, 1)}")

# --- TEST ALANI ---
if __name__ == "__main__":
    calc = StatCalculator()
    
    # Test: Jinx'e full build dizelim
    # Not: Eşya isimleri Riot veritabanındaki ile birebir aynı olmalı (Türkçe indirdiğimiz için Türkçe yazıyoruz)
    test_champ = "Jinx"
    test_items = [
        "Ebedi Kılıç",     # Infinity Edge
        "Kraken Katili",   # Kraken Slayer
        "Kana Susamış",    # Bloodthirster
        "Dominik Efendi'nin Hürmetleri" # LDR
    ]
    
    calc.calculate_build(test_champ, test_items)