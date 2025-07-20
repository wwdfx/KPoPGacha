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

# Card data from the provided file
cards_data = [
    # Up ver (Selfie set)
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Heeseung", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923491edae80600970.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Jay", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923493c0e489fa0319.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Jake", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923495a1b5cd17acaf.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Sunghoon", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923497612640851e33.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Sunoo", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392349923041b8a8886.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Jungwon", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392349ab5668dea07bf.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Ni-ki", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392349c5d689782f51f.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Selfie set)", "Group", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392639ae1b4dc3fc217.png"),
    
    # Up ver (Concept set)
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Heeseung", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392349de8ec432c5965.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Jay", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392349f95b6276ea06a.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Jake", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234a16f1342ecbf0d.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Sunghoon", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67a82ead0020d0231921.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Sunoo", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234a512d38e941ad6.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Jungwon", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234a6dffd7c09d797.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Up ver (Concept set)", "Ni-ki", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234a88cf915a39180.png"),
    
    # Hype ver (Selfie set)
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Heeseung", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67a830b5003d0695f94a.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Jay", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234b83b3d57f6dddd.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Jake", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234ba02530c67704c.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Sunghoon", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234bbbb4d3ad6a6f8.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Sunoo", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234bd71441aba1a56.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Jungwon", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234bf5357f2e6bd9b.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Ni-ki", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234c15ff87f2a2595.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Selfie set)", "Group", "Эпическая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392639c94e9091ab07b.png"),
    
    # Hype ver (Concept set)
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Heeseung", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234c32058f9b0a2e7.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Jay", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234c507370f4c4fae.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Jake", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234c6db8a9f0850f7.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Sunghoon", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234c87a583521f93c.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Sunoo", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234ca095045e11f75.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Jungwon", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234cb892c096cc99c.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Hype ver (Concept set)", "Ni-ki", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234cd35612e7ab82d.png"),
    
    # Down ver (Selfie set)
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Heeseung", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234daa28612f9a24f.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Jay", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234dc509ecde59449.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Jake", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234ddeec2242a2dc6.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Sunghoon", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234e004bcfe85d3f2.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Sunoo", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234e1dcc63aa03f2d.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Jungwon", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234e387e8a17e7954.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Ni-ki", "Обычная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234e58da7baab7f9e.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Selfie set)", "Group", "Эпическая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392639e1b93f96c5848.png"),
    
    # Down ver (Concept set)
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Heeseung", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234e75ecb06caa8e6.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Jay", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234e8ebca103ab77b.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Jake", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234eab7d4d6e59b2a.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Sunghoon", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67a8311a002f9007bd7e.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Sunoo", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234ee42cd105b116e.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Jungwon", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234f00c9b70c85617.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Down ver (Concept set)", "Ni-ki", "Редкая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639234f1a5ef3c8bebd4.png"),
    
    # Weverse Shop Preorder
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Heeseung", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239e897dcbe97a533.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Jay", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239ea4786cf62104d.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Jake", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239ebe45a9036ea38.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Sunghoon", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239edba070825f3e0.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Sunoo", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239ef6e961990689a.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Jungwon", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239f12629fa893421.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Ni-ki", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239f443f4633085de.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Unit A", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926531d43356c1439a.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Weverse Shop Preorder", "Unit B", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63926533748a1f2f2efa.png"),
    
    # Soundwave Lucky Draw
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Heeseung", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923eac0969e76f1e4e.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Jay", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923eaf5bfec31ca465.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Jake", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923eb28a7e3281d6dc.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Sunghoon", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923eb5f06fa83ff19b.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Sunoo", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256d845c4aa6467e0.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Jungwon", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256db4abccbdbec09.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Soundwave Lucky Draw", "Ni-ki", "Легендарная", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256de427150537dd3.png"),
    
    # Powerstation Lucky Draw
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Heeseung", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256f6ebd54157bae9.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Jay", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256fa1b3caa24da31.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Jake", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639256fe7512a8d1942b.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Sunghoon", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639257032a4a36fcf018.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Sunoo", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925707ce9e65629ee7.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Jungwon", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392570d186dc9c7d690.png"),
    ("Enhypen", "BORDER: CARNIVAL", "Powerstation Lucky Draw", "Ni-ki", "Полая", "https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6776233300209986c771.png"),
]

def main():
    success_count = 0
    error_count = 0
    
    print(f"Starting import of {len(cards_data)} Enhypen cards...")
    
    for i, (group, album, version, position, rarity_text, image_url) in enumerate(cards_data, 1):
        # Create card name (you can modify this format as needed)
        name = f"{group} - {position} ({version})"
        
        # Map rarity to number
        rarity_value = rarity_mapping.get(rarity_text, 1)
        
        # Handle the lambda function for 'Обычная' (Common) rarity
        if callable(rarity_value):
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