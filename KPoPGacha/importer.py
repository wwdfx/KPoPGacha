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
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Heeseung	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256e1226f1b41af1a.png
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Jay	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256e43d4122aa2c28.png
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Jake	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256e77d3d713d8591.png
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Sunghoon	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256eaa98966cfead7.png
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Sunoo	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256edc63eb6ce496f.png
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Jungwon	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256f0cff27a423c36.png
Enhypen 	BORDER: CARNIVAL	M2U Lucky Draw	Ni-ki	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256f3ce3b0040c4ef.png
					
					
Enhypen 	BORDER: HAKANAI	Standart ver	Heeseung	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/644e2f1f3a79683731b5.png
Enhypen 	BORDER: HAKANAI	Standart ver	Jay	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/644e2ea89d69a719b88a.png
Enhypen 	BORDER: HAKANAI	Standart ver	Jake	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761a3f0002f415979f.png
Enhypen 	BORDER: HAKANAI	Standart ver	Sunghoon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761a5a0016c64eff9e.png
Enhypen 	BORDER: HAKANAI	Standart ver	Sunoo	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761aa00002a575879f.png
Enhypen 	BORDER: HAKANAI	Standart ver	Jungwon	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761abc0017db0cac6b.png
Enhypen 	BORDER: HAKANAI	Standart ver	Ni-ki	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd3b14e0d01297117.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Heeseung	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd4a21d5a7dbe1024.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Jay	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd4b4d2e62eb7d918.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Jake	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761b2300010bc38ec8.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Sunghoon	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd4dad3adf9d5aada.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Sunoo	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd4eb6ae34f7701ad.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Jungwon	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd4fee758f51ad594.png
Enhypen 	BORDER: HAKANAI	Universal Music Store Set	Ni-ki	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd51030d3517b9171.png
Enhypen 	BORDER: HAKANAI	Heeseung ver	Heeseung A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd56b123828a100f2.png
Enhypen 	BORDER: HAKANAI	Heeseung ver	Heeseung B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd57db43e1edd405b.png
Enhypen 	BORDER: HAKANAI	Jay ver	Jay A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd59c832e58302a1c.png
Enhypen 	BORDER: HAKANAI	Jay ver	Jay B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd5ae8bc53530205d.png
Enhypen 	BORDER: HAKANAI	Jake ver	Jake A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd5c5e475079ef03f.png
Enhypen 	BORDER: HAKANAI	Jake ver	Jake B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd5d7a52a7be42bde.png
Enhypen 	BORDER: HAKANAI	Sunghoon ver	Sunghoon A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd5ef05203366515b.png
Enhypen 	BORDER: HAKANAI	Sunghoon ver	Sunghoon B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761cee000ac967a521.png
Enhypen 	BORDER: HAKANAI	Sunoo ver	Sunoo A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd61f4ffac7dcc5b0.png
Enhypen 	BORDER: HAKANAI	Sunoo ver	Sunoo B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/687b918c002fac695a17.png
Enhypen 	BORDER: HAKANAI	Jungwon ver	Jungwon A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd536b450f6dd22ab.png
Enhypen 	BORDER: HAKANAI	Jungwon ver	Jungwon B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761cc2002de989defd.png
Enhypen 	BORDER: HAKANAI	Ni-ki ver	Ni-ki	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67761d89002d489bbdea.png
Enhypen 	BORDER: HAKANAI	Ni-ki ver	Ni-ki	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd66bdda67e659d1d.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Heeseung A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/677623c200122c00596a.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Heeseung B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddac4c7e93b9c32f2.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Jay A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddad4030ff2e62725.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Jay B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddae15a3200058636.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Jake A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddaede0e93269f219.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Jake B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddafb8c16355637a0.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Sunghoon A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb0c295a2a6326eb.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Sunghoon B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb1a7e6c5320582f.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Sunoo A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb27eec85fe4659d.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Sunoo B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb38b3d82ac977e6.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Jungwon A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb488eee4a6ba9c7.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Jungwon B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb55b53dec527b60.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Ni-ki A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb6531df4a52f89c.png
Enhypen 	BORDER: HAKANAI	Weverse/UMS Lucky Draw	Ni-ki B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ddb71f41842c48f00.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Heeseung	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd6dfc4f7e1627406.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Jay	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/683fb6f20010ab24d00e.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Jake	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd71637764f48c058.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Sunghoon	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd7332146eccedb0c.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Sunoo	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/683fb53f0010bcd89142.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Jungwon	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd768f388421bdbbe.png
Enhypen 	BORDER: HAKANAI	Tower Records Lucky Draw	Ni-ki	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641dd77c84606f28867c.png
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