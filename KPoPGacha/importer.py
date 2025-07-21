import requests
import json
import random

# PocketBase configuration
POCKETBASE_URL = 'http://127.0.0.1:8092'
COLLECTION_NAME = 'cards'

class PocketBase:
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.session = requests.Session()
    
    def create_record(self, collection, data):
        """Create a new record in the specified collection"""
        endpoint = f"{self.url}/api/collections/{collection}/records"
        response = self.session.post(endpoint, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error creating record: {response.status_code} - {response.text}")
            return None

# Initialize PocketBase
pb = PocketBase(POCKETBASE_URL)

# Updated rarity mapping from Russian to numbers
rarity_mapping = {
    'Обычная': lambda: random.choice([1, 2]),  # Common - random 1 or 2
    'Редкая': 3,       # Rare
    'Эпическая': 4,    # Epic
    'Легендарная': 5,  # Legendary
    'Полая': 6         # Hollow/Special
}

# Card data as a raw string
# To use, paste the tab-separated card data between the triple quotes.
input_text = """
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Heeseung	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253df9b08d7b65b32.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Jay	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253e1271b999fc15d.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Jake	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253e29c396d041b03.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Sunghoon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253e42d1ebbd90071.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Sunoo	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253e5df7e4ffde63d.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Jungwon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253e7afd3331b167b.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Ni-ki	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639253e951ab7d2fc2f2.png
Enhypen 	DIMENSION: DILEMMA 	Scylla ver	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392639fc0b5d5fbb520.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Heeseung	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925230850adab9288b.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Jay	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392525d19827db85332.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Jake	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67771dc0001cbabd0956.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Sunghoon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392526021dd5d4e02e9.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Sunoo	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925261aa701b04666a.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Jungwon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392526331e29866e0cc.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Ni-ki	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925264cd592510cd26.png
Enhypen 	DIMENSION: DILEMMA 	Odysseus ver	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639263a1be80a3072384.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Heeseung	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254009b1a1dc59c69.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Jay	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254022ac1eb08ab8b.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Jake	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925403c370316e8498.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Sunghoon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925405cda464f22852.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Sunoo	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254076a4766c0e9e5.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Jungwon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925408cfb3f56a7308.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Ni-ki	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392540a6e2dcd7017e9.png
Enhypen 	DIMENSION: DILEMMA 	Charybdis ver	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639263a35f355c14e3ca.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Heeseung A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639252363e244b0e0983.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Heeseung B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925237cb159119e549.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Heeseung C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392523972d47ada4a36.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jay A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925257b2f24badae34.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jay B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392541c611dc4fc08db.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jay C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392542eb03129733f87.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jake A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925259d67fcff8f5c7.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jake B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392541dcdc736004bca.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jake C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254303d49cd1c9dc6.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Sunghoon A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392525b90cba8195337.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Sunghoon B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392541f5145e2524219.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Sunghoon C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254303d49cd1c9dc6.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Sunoo A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925417a47724ea6cb0.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Sunoo B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254209e005f80f897.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Sunoo C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392543366001326aa3d.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jungwon A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254194d97305e4a66.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jungwon B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392542225d9aa5506fe.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Jungwon C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925434e5839ccfa42e.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Ni-ki A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392541ad0cb94289b77.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Ni-ki B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639254239bf79fc46559.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Ni-ki C	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392543667dd097a8331.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Group A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639263a53222061c4911.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Group B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639263a8016be819478d.png
Enhypen 	DIMENSION: DILEMMA 	Essential ver	Group C	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639263a9dcc434b6d27e.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Heeseung	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639265cda8525cc4a7f0.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Jay	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639265cf1c39b0386ff4.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Jake	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639265d08f6dc0e6dc7f.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Sunghoon	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639265d64edec56a4f05.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Sunoo	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/677618fe0006807ce323.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Jungwon	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/677618fe0006807ce323.png
Enhypen 	DIMENSION: DILEMMA 	Apple Music Postcard	Ni-ki	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639265dc24056e2e1086.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Heeseung 	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6427626c35f16bb9558d.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Jay	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/642762a59165383cccaf.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Jake	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/642762b784524199c7fc.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Sunghoon	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/642762c5e857568d5283.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Sunoo	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/677618ab001732779c15.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Jungwon	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/642762f5d614960c2b67.png
Enhypen 	DIMENSION: DILEMMA 	Shopee	Ni-ki	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/642763047c65ce48163d.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Heeseung	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e7a95f9342d8207.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Jay	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e7c816387ed6f6b.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Jake	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e7e48010bfd5b38.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Sunghoon	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e7fdb43c0fe5d18.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Sunoo	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e8176b4d8bc071c.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Jungwon	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e8355e01935ec1f.png
Enhypen 	DIMENSION: DILEMMA 	Naver Shopping Live	Ni-ki	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926e85081579ab63af.png
"""

def parse_input_to_cards(text):
    """Parses tab-separated text into a list of card tuples."""
    cards = []
    lines = text.strip().split('\n')
    for line in lines:
        # Skip empty or whitespace-only lines
        if not line.strip():
            continue
        
        parts = [part.strip() for part in line.split('\t')]
        
        # Ensure the line has the correct number of parts
        if len(parts) == 6:
            cards.append(tuple(parts))
        else:
            print(f"⚠️ Skipping malformed line: {line}")
            
    return cards

def main():
    # Parse the text input into card data
    cards_data = parse_input_to_cards(input_text)

    if not cards_data:
        print("No card data found in the input text. Exiting.")
        return

    success_count = 0
    error_count = 0
    
    print(f"Starting import of {len(cards_data)} Enhypen cards...")
    
    for i, (group, album, version, position, rarity_text, image_url) in enumerate(cards_data, 1):
        # Create card name (you can modify this format as needed)
        name = f"{group} - {position} ({version})"
        
        # Map rarity to number
        rarity_value = rarity_mapping.get(rarity_text)
        if rarity_value is None:
            print(f"⚠️ Rarity '{rarity_text}' not found for '{name}'. Defaulting to 1.")
            rarity = 1
        # Handle the lambda function for 'Обычная' (Common) rarity
        elif callable(rarity_value):
            rarity = rarity_value()  # Call the lambda function to get random 1 or 2
        else:
            rarity = rarity_value
        
        # Prepare the data for PocketBase
        data = {
            "name": name,
            "group": group,
            "rarity": rarity,
            "image_url": image_url,
            "position": position,
            "stats": "{}",  # Empty JSON object as string
            "album": album,
            "version": version
        }
        
        # Create the record
        result = pb.create_record(COLLECTION_NAME, data)
        
        if result:
            print(f"✅ [{i}/{len(cards_data)}] Created: {name} (Rarity: {rarity})")
            success_count += 1
        else:
            print(f"❌ [{i}/{len(cards_data)}] Failed: {name}")
            error_count += 1
    
    print(f"\n📊 Import completed!")
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📋 Total: {len(cards_data)}")

if __name__ == "__main__":
    main() 