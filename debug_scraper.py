import requests
from bs4 import BeautifulSoup
from lol_library import ChampionLibrary

def debug_url():
    # Senin verdiğin o sorunlu link
    url = "https://www.aramonly.com/guide/fiddlesticks/tank-build"
    
    print(f"--- RÖNTGEN BAŞLIYOR: {url} ---")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers)
        print(f"Bağlantı Durumu: {response.status_code}")
        
        if response.status_code != 200:
            print("Sayfa açılamadı!")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("\n--- SAYFADA BULUNAN RESİM YAZILARI (ALT TAGS) ---")
        found_count = 0
        
        # Kütüphaneyi yükle ki karşılaştırma yapabilelim
        lib = ChampionLibrary()
        
        for img in soup.find_all('img'):
            alt_text = img.get('alt')
            if alt_text:
                # Ekrana yazdıralım bakalım ne görüyor?
                rune_id = lib.get_rune_id(alt_text)
                status = f"✅ (ID: {rune_id})" if rune_id else "❌ (Tanınmadı)"
                
                print(f"Bulunan: '{alt_text}' -> {status}")
                found_count += 1
                
        print(f"\nToplam {found_count} resim tarandı.")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    debug_url()