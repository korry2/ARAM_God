import json

def search_item(keyword):
    """Verilen kelimeyi eşya isimlerinde arar."""
    try:
        with open("data/item.json", "r", encoding="utf-8") as f:
            data = json.load(f)["data"]
            
        print(f"\n--- '{keyword}' İÇİN ARAMA SONUÇLARI ---")
        found_count = 0
        
        for item_id, item_data in data.items():
            # Büyük/küçük harf duyarlılığını kaldırmak için ikisini de küçültüyoruz
            if keyword.lower() in item_data["name"].lower():
                print(f"Bulundu: {item_data['name']}")
                found_count += 1
                
        if found_count == 0:
            print("Sonuç bulunamadı.")
        else:
            print(f"Toplam {found_count} eşleşme.")

    except FileNotFoundError:
        print("HATA: data/item.json dosyası bulunamadı.")

if __name__ == "__main__":
    # "Kana" kelimesini arayarak doğrusunu bulalım
    search_item("Kana")