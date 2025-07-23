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
TXT	The Dream Chapter: Star	Blue Back Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737871e0019e18883d3.png
TXT	The Dream Chapter: Star	Blue Back Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737870d002fe4af96d6.png
TXT	The Dream Chapter: Star	Blue Back Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673786fe00314607860c.png
TXT	The Dream Chapter: Star	Blue Back Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737874a00125b1d2680.png
TXT	The Dream Chapter: Star	Blue Back Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673786e00000833c9065.png
TXT	The Dream Chapter: Star	White Back Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737879600301a42fce6.png
TXT	The Dream Chapter: Star	White Back Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67378787001ea3280bb2.png
TXT	The Dream Chapter: Star	White Back Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67378901002bcd5c27f1.png
TXT	The Dream Chapter: Star	White Back Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737883e00057364ad0e.png
TXT	The Dream Chapter: Star	White Back Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737885f003a78bca3a0.png
TXT	The Dream Chapter: Magic	Student ID Pad Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737947e0016094e0203.png
TXT	The Dream Chapter: Magic	Student ID Pad Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673793f70014eb5bff94.png
TXT	The Dream Chapter: Magic	Student ID Pad Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737958b0019e6980d51.png
TXT	The Dream Chapter: Magic	Student ID Pad Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673795aa00043e76d59a.png
TXT	The Dream Chapter: Magic	Student ID Pad Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673795bf001aef971ecf.png
TXT	The Dream Chapter: Magic	Keyring Photocard Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737828d0004849cda99.png
TXT	The Dream Chapter: Magic	Keyring Photocard Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737822a0034ba532b0f.png
TXT	The Dream Chapter: Magic	Keyring Photocard Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673782e2002365434ddc.png
TXT	The Dream Chapter: Magic	Keyring Photocard Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673783230029236453d0.png
TXT	The Dream Chapter: Magic	Keyring Photocard Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67378366000f5ce72357.png
TXT	The Dream Chapter: Magic	Arcadia Student ID Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc93100007757ccf76.png
TXT	The Dream Chapter: Magic	Arcadia Student ID Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc93b70024f0d6a09f.png
TXT	The Dream Chapter: Magic	Arcadia Student ID Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc935c002d1a60c85c.png
TXT	The Dream Chapter: Magic	Arcadia Student ID Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc92e9000027b315e9.png
TXT	The Dream Chapter: Magic	Arcadia Student ID Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc922d000c6cde1610.png
TXT	The Dream Chapter: Magic	Sanctuary Student ID Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63920c3c29868b234af4.png
TXT	The Dream Chapter: Magic	Sanctuary Student ID Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc90fa0025981a6df5.png
TXT	The Dream Chapter: Magic	Sanctuary Student ID Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63920c3d71e43c700621.png
TXT	The Dream Chapter: Magic	Sanctuary Student ID Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63920c3eba5be5af9f86.png
TXT	The Dream Chapter: Magic	Sanctuary Student ID Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc925000114efba753.png
TXT	The Dream Chapter: Magic	Soundwave 2023 Reissue Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c0a403000b92da3688.png
TXT	The Dream Chapter: Magic	Soundwave 2023 Reissue Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c0a455002365f83775.png
TXT	The Dream Chapter: Magic	Soundwave 2023 Reissue Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c0a48800287d32acca.png
TXT	The Dream Chapter: Magic	Soundwave 2023 Reissue Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c0a4d50036cf681167.png
TXT	The Dream Chapter: Magic	Soundwave 2023 Reissue Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c0a518002b5a476013.png
TXT	The Dream Chapter: Magic	Soundwave 2023 Reissue Lucky Draw	Group	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6833c9270037c39191f3.png
TXT	Magic Hour	Weply Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223eb2b580cc15a82.png
TXT	Magic Hour	Weply Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223e99d354c3d5990.png
TXT	Magic Hour	Weply Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223ed0d30aa7fb960.png
TXT	Magic Hour	Weply Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223ee5ed3e89b9f8c.png
TXT	Magic Hour	Weply Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223efae77578948f2.png
TXT	Magic Hour	Universal Music Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673308ef002beb19b23e.png
TXT	Magic Hour	Universal Music Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673309930013f54216d4.png
TXT	Magic Hour	Universal Music Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673309be002f25e302f1.png
TXT	Magic Hour	Universal Music Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67330cf80010b6bcc866.png
TXT	Magic Hour	Universal Music Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67330d24000e260cb6e3.png
TXT	Magic Hour	Official Japan Store Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc9bd100124594b055.png
TXT	Magic Hour	Official Japan Store Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223f0f00a9b95701c.png
TXT	Magic Hour	Official Japan Store Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc9c840039e6c775c8.png
TXT	Magic Hour	Official Japan Store Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639223f516bb88fd56cd.png
TXT	Magic Hour	Official Japan Store Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66bc9cac003124faa8fc.png
TXT	The Dream Chapter: Eternity	Port Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379bf100281b3deea7.png
TXT	The Dream Chapter: Eternity	Port Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379bff000100013a33.png
TXT	The Dream Chapter: Eternity	Port Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379c0c001f5bc92550.png
TXT	The Dream Chapter: Eternity	Port Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379c19002e06607183.png
TXT	The Dream Chapter: Eternity	Port Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379c28002a5e6280f8.png
TXT	The Dream Chapter: Eternity	Port Set	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379c38000c2d9f596c.png
TXT	The Dream Chapter: Eternity	Clear Card Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379a4600324664bc22.png
TXT	The Dream Chapter: Eternity	Clear Card Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673799370012012dfeee.png
TXT	The Dream Chapter: Eternity	Clear Card Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737994a00372c3d04ea.png
TXT	The Dream Chapter: Eternity	Clear Card Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737995b0013cba569e7.png
TXT	The Dream Chapter: Eternity	Clear Card Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673799a7000c9c35fd92.png
TXT	The Dream Chapter: Eternity	TU Illust Card	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d66ebf000e7301f711.png
TXT	The Dream Chapter: Eternity	Starboard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379b8c0023bddba88e.png
TXT	The Dream Chapter: Eternity	Starboard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379b9c002d4de3d623.png
TXT	The Dream Chapter: Eternity	Starboard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379bad0016d2b71454.png
TXT	The Dream Chapter: Eternity	Starboard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379bbd000e5d4db385.png
TXT	The Dream Chapter: Eternity	Starboard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67379bce000abf066ad3.png
TXT	The Dream Chapter: Eternity	Starboard Set	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737972b0001a476fa80.png
TXT	The Dream Chapter: Eternity	Withfans Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639224406bd3351aaabb.png
TXT	The Dream Chapter: Eternity	Withfans Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392243f247e68391e84.png
TXT	The Dream Chapter: Eternity	Withfans Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63922441bec956204d63.png
TXT	The Dream Chapter: Eternity	Withfans Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63922442e88471d1df0f.png
TXT	The Dream Chapter: Eternity	Withfans Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63922444498549f16df3.png
TXT	The Dream Chapter: Eternity	Withfans Preorder	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392245064e65b608602.png
TXT	The Dream Chapter: Eternity	Soundwave Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28bfe0027d36279ef.png
TXT	The Dream Chapter: Eternity	Soundwave Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d67cb400265e1768bf.png
TXT	The Dream Chapter: Eternity	Soundwave Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28c12002c4beedf0e.png
TXT	The Dream Chapter: Eternity	Soundwave Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28ba90027a10b7ab5.png
TXT	The Dream Chapter: Eternity	Soundwave Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28c260008a7733731.png
TXT	The Dream Chapter: Eternity	M2U Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28a6d00288a028e94.png
TXT	The Dream Chapter: Eternity	M2U Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28a440002ed6eed7e.png
TXT	The Dream Chapter: Eternity	M2U Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28a8d003c5a140928.png
TXT	The Dream Chapter: Eternity	M2U Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28acc001bec7c7970.png
TXT	The Dream Chapter: Eternity	M2U Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c28aa90011bc2a85f1.png
TXT	The Dream Chapter: Eternity	Soundwave 2023 Reissue Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c290fc00255734eeba.png
TXT	The Dream Chapter: Eternity	Soundwave 2023 Reissue Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c2912e0030f2aa8582.png
TXT	The Dream Chapter: Eternity	Soundwave 2023 Reissue Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c29154003d5fc67ef8.png
TXT	The Dream Chapter: Eternity	Soundwave 2023 Reissue Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c291980029f3c558fb.png
TXT	The Dream Chapter: Eternity	Soundwave 2023 Reissue Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c291ce003dcf2ead05.png
TXT	The Dream Chapter: Eternity	Soundwave 2023 Reissue Lucky Draw	Group	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c291fd00378d7a225e.png
TXT	Drama	Universal Music Japan Preorder Postcards	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673352e90011e56e9b03.png
TXT	Drama	Universal Music Japan Preorder Postcards	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67335315002f20b129ce.png
TXT	Drama	Universal Music Japan Preorder Postcards	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6733533d0025065c957c.png
TXT	Drama	Universal Music Japan Preorder Postcards	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6733535f00375ebfa4b9.png
TXT	Drama	Universal Music Japan Preorder Postcards	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67335380000f466ca58f.png
TXT	Drama	Tower Records Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6733392c001fada5b276.png
TXT	Drama	Tower Records Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673339730001234ed076.png
TXT	Drama	Tower Records Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673339a9003e27540501.png
TXT	Drama	Tower Records Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673339d30005c79fb3e8.png
TXT	Drama	Tower Records Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67333a03002a4cf1811a.png
TXT	Drama	WOWOW x TXT Japan FC Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925225cfd5d11bff21.png
TXT	Drama	WOWOW x TXT Japan FC Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639252246bdfd1239ee5.png
TXT	Drama	WOWOW x TXT Japan FC Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639252272804d833223c.png
TXT	Drama	WOWOW x TXT Japan FC Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63925228a2053e86c5a3.png
TXT	Drama	WOWOW x TXT Japan FC Preorder	Hueningkai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392522a1a248dbc1260.png
TXT	Drama	Weverse Global Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a3860003a4eb8a27.png
TXT	Drama	Weverse Global Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a35b002694fdb468.png
TXT	Drama	Weverse Global Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639224330630d6caaee0.png
TXT	Drama	Weverse Global Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63922434768a1e24ec68.png
TXT	Drama	Weverse Global Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a3b50035d4c92150.png
TXT	Minisode 1: Blue Hour	R Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392289b55ecbbeb1b14.png
TXT	Minisode 1: Blue Hour	R Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63922899b683662111c7.png
TXT	Minisode 1: Blue Hour	R Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392289d1259ce86dffc.png
TXT	Minisode 1: Blue Hour	R Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392289e382d14b699e4.png
TXT	Minisode 1: Blue Hour	R Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392289f7cf7c41163b4.png
TXT	Minisode 1: Blue Hour	AR Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228a297e223cbac6e.png
TXT	Minisode 1: Blue Hour	AR Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228a1170183d04ff5.png
TXT	Minisode 1: Blue Hour	AR Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228a3e846010bf021.png
TXT	Minisode 1: Blue Hour	AR Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228a56744bdaf5b69.png
TXT	Minisode 1: Blue Hour	AR Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228a69288d8b40160.png
TXT	Minisode 1: Blue Hour	VR Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228a8d05b6f15b805.png
TXT	Minisode 1: Blue Hour	VR Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5208e000891013778.png
TXT	Minisode 1: Blue Hour	VR Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639228aa1632a02e94ac.png
TXT	Minisode 1: Blue Hour	VR Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c520ff002938a530b9.png
TXT	Minisode 1: Blue Hour	VR Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c521270018be783bc1.png
TXT	Minisode 1: Blue Hour	Weverse Global Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d505c200200fd2cb77.png
TXT	Minisode 1: Blue Hour	Weverse Global Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4f77e002eb007b3b0.png
TXT	Minisode 1: Blue Hour	Weverse Global Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d506ce001a4be54a6d.png
TXT	Minisode 1: Blue Hour	Weverse Global Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50605002c99332df3.png
TXT	Minisode 1: Blue Hour	Weverse Global Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5074f000699003408.png
TXT	Minisode 1: Blue Hour	Weverse Global Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d508ec0010b5ae0aee.png
TXT	Minisode 1: Blue Hour	Weverse Global Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50671001605d8d87e.png
TXT	Minisode 1: Blue Hour	Weverse Global Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4fba6001cf1d5af08.png
TXT	Minisode 1: Blue Hour	Weverse Global Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50576002e4c7d30e0.png
TXT	Minisode 1: Blue Hour	Weverse Global Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4f98d0019096b56ad.png
TXT	Minisode 1: Blue Hour	Target Exclusive	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923506d584c6dafab3.png
TXT	Minisode 1: Blue Hour	Mecima Online Fansign	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4d5f4002fe0cda47e.png
TXT	Minisode 1: Blue Hour	Mecima Online Fansign	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4d68d00153e42dd25.png
TXT	Minisode 1: Blue Hour	Mecima Online Fansign	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4da62000c64d46812.png
TXT	Minisode 1: Blue Hour	Mecima Online Fansign	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4d778003b08cd2b5a.png
TXT	Minisode 1: Blue Hour	Mecima Online Fansign	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4d7c20021f6873fe9.png
TXT	Minisode 1: Blue Hour	Withfans 1.0 Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50caa003c4787cfa7.png
TXT	Minisode 1: Blue Hour	Withfans 1.0 Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50b76002e683f0789.png
TXT	Minisode 1: Blue Hour	Withfans 1.0 Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50bcf00169b955557.png
TXT	Minisode 1: Blue Hour	Withfans 1.0 Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50c2b0005ec7985e3.png
TXT	Minisode 1: Blue Hour	Withfans 1.0 Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d50d14001a6807d49d.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392395b168332838894.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239594009c517b2aa.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392395cc3296214fbf2.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392395f2399c44981da.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923960c45747daf62d.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4ecaa0035dd52a45b.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4ecd70027a525b8f8.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4ed110034cf0f7d43.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923962bd54f0fb2083.png
TXT	Minisode 1: Blue Hour	Withfans 2.0 Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d4ed3a001a0be233d6.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Soobin A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d536f400372815d042.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Soobin B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53735002dfc09f93b.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Yeonjun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d534dd00353d5f668f.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Yeonjun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d518d70021a43249ff.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Beomgyu A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d539bb0037ead503ab.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Beomgyu B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d539ec0035ebc3540b.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Taehyun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d542110019d4d057a6.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Taehyun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5423100323af3724a.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Huening Kai A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d542a5003113759261.png
TXT	Minisode 1: Blue Hour	Soundwave 1.0 Lucky Draw	Huening Kai B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d542be00036a8042f9.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Soobin A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5383e00038ca314e5.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Soobin B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5389600214f6cf64a.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Soobin C	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d538e5003c8c1ab760.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Yeonjun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5350f002de9860cad.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Yeonjun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5129f0016a06e246a.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Yeonjun C	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53539001b49ee364f.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Beomgyu A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53a99003d2b601a9e.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Beomgyu B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/640cd55b4c7bb3d7f5a7.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Beomgyu C	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53aef00021e16c458.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Taehyun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53bdb003972dcc637.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Taehyun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53c02002e0c25a064.png
TXT	Minisode 1: Blue Hour	Soundwave 2.0 Lucky Draw	Taehyun C	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53c1b0024bbbad46e.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Soobin A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d537e200337aa79c43.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Soobin B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5380500389e7d920f.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Yeonjun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5154100398c1599bd.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Yeonjun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5359a00048e15d2cc.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Beomgyu A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53a350012f3bbd938.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Beomgyu B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d53a66003754dd1f16.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Taehyun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d542630015990bd226.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Taehyun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d54279002e1e7817fa.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Huening Kai A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d54310001605b7fb85.png
TXT	Minisode 1: Blue Hour	M2U 1.0 Lucky Draw	Huening Kai B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d5432c000ad0122aae.png
TXT	Minisode 1: Blue Hour	Soundwave 2023 Reissue Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d62634001a7ee86a9b.png
TXT	Minisode 1: Blue Hour	Soundwave 2023 Reissue Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d51e0e000f4e4753a0.png
TXT	Minisode 1: Blue Hour	Soundwave 2023 Reissue Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6243f001d00c1e9e7.png
TXT	Minisode 1: Blue Hour	Soundwave 2023 Reissue Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6229b0007d5621057.png
TXT	Minisode 1: Blue Hour	Soundwave 2023 Reissue Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d62382000ee54f5e3d.png
TXT	Minisode 1: Blue Hour	Soundwave 2023 Reissue Lucky Draw	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d62545002d724d2582.png
TXT	Still Dreaming	1st Press Standard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392355bb651c6aa5cb0.png
TXT	Still Dreaming	1st Press Standard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392355a322b24d9d00d.png
TXT	Still Dreaming	1st Press Standard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6827700258fff1d7b.png
TXT	Still Dreaming	1st Press Standard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392355d8d4b81a47f66.png
TXT	Still Dreaming	1st Press Standard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392355f410ac1dd2ce7.png
TXT	Still Dreaming	Weverse Japan Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40ba500396d99caa6.png
TXT	Still Dreaming	Weverse Japan Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40c1d002b95ab02f4.png
TXT	Still Dreaming	Weverse Japan Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/640cd4e959d73be62981.png
TXT	Still Dreaming	Weverse Japan Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639281cad90046032289.png
TXT	Still Dreaming	Weverse Japan Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40b5c0023968fc511.png
TXT	Still Dreaming	Universal Music Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40cce000f15339ed4.png
TXT	Still Dreaming	Universal Music Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40cea00042feb7a8a.png
TXT	Still Dreaming	Universal Music Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/640c9f7839f6ffe6ddf1.png
TXT	Still Dreaming	Universal Music Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392356187c1cff95cdc.png
TXT	Still Dreaming	Universal Music Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40d0e0005570bc345.png
TXT	Still Dreaming	HMV Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40f420019b598874c.png
TXT	Still Dreaming	HMV Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40f130023162c0d64.png
TXT	Still Dreaming	HMV Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40df800178d1b9b60.png
TXT	Still Dreaming	HMV Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40a69001ba9bb72dc.png
TXT	Still Dreaming	HMV Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c40f2600295b974666.png
TXT	Still Dreaming	Tower Records Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6b7a9000a78d71d8b.png
TXT	Still Dreaming	Tower Records Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6b48b000ed6ffcb63.png
TXT	Still Dreaming	Tower Records Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6b4a8001f03b63bb7.png
TXT	Still Dreaming	Tower Records Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6b8d70002d3d6537d.png
TXT	Still Dreaming	Tower Records Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d6b5b8000bb3fdfff6.png
TXT	Still Dreaming	Weverse Global Preorder Group Postcards	Group A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d7ecb500156809d59a.png
TXT	Still Dreaming	Weverse Global Preorder Group Postcards	Group B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d7ece2001fd42532aa.png
TXT	Still Dreaming	Tower Records Shibuya Exclusive Lucky Draw Postcards	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a47a0005f1aadecf.png
TXT	Still Dreaming	Tower Records Shibuya Exclusive Lucky Draw Postcards	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737abea0011cd6614a2.png
TXT	Still Dreaming	Tower Records Shibuya Exclusive Lucky Draw Postcards	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a4b500187b1c0270.png
TXT	Still Dreaming	Tower Records Shibuya Exclusive Lucky Draw Postcards	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a520001c980a401e.png
TXT	Still Dreaming	Tower Records Shibuya Exclusive Lucky Draw Postcards	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737a59e001627d548c4.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Soobin A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d803b800398e40a17d.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Soobin B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d805890017f418a7cf.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Yeonjun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d804be001dfbf88586.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Yeonjun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d81925001cefa6c08d.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Beomgyu A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d803a1001142699c2d.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Beomgyu B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d81bb70015137ee75e.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Taehyun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d81a59003e3671f394.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Taehyun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d81c8a002eaf7f17dd.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Huening Kai A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d80385003b48858a94.png
TXT	Still Dreaming	Omikuji Lucky Draw Postcards	Huening Kai B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66d81845000e78ca81aa.png
TXT	The Chaos Chapter: Freeze	World Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639235312abce43ddbe8.png
TXT	The Chaos Chapter: Freeze	World Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392352f6b43262bf7ca.png
TXT	The Chaos Chapter: Freeze	World Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923532addf8fe1f773.png
TXT	The Chaos Chapter: Freeze	World Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923534460204a00ddf.png
TXT	The Chaos Chapter: Freeze	World Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392353601c5796d2872.png
TXT	The Chaos Chapter: Freeze	Soundwave 2.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbddac002b1656e6ee.png
TXT	The Chaos Chapter: Freeze	Soundwave 2.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbddcc00024bdf7d87.png
TXT	The Chaos Chapter: Freeze	Soundwave 2.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbddf400046e6786b6.png
TXT	The Chaos Chapter: Freeze	Soundwave 2.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbde1f002c1b3056e5.png
TXT	The Chaos Chapter: Freeze	Soundwave 2.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbde56002e6649ac97.png
TXT	The Chaos Chapter: Freeze	Soundwave 2.0 Lucky Draw	Group Postcard	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db1db00021b4774af0.png
TXT	The Chaos Chapter: Freeze	M2U 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db44c80025ab6594d5.png
TXT	The Chaos Chapter: Freeze	M2U 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db29a9002450b42713.png
TXT	The Chaos Chapter: Freeze	M2U 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db4586001915df2525.png
TXT	The Chaos Chapter: Freeze	M2U 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db46000033a1532343.png
TXT	The Chaos Chapter: Freeze	M2U 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392c9bf4d65c89137ad.png
TXT	The Chaos Chapter: Freeze	Shopee Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dba1d0000ce846d34d.png
TXT	The Chaos Chapter: Freeze	Shopee Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db99db0026e729f318.png
TXT	The Chaos Chapter: Freeze	Shopee Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dba32b000e6757988c.png
TXT	The Chaos Chapter: Freeze	Shopee Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dba4ac001f2586f9a5.png
TXT	The Chaos Chapter: Freeze	Shopee Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db9c82002f9b567ed5.png
TXT	The Chaos Chapter: Freeze	Weverse Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392350a112492781447.png
TXT	The Chaos Chapter: Freeze	Weverse Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639235086342401d493e.png
TXT	The Chaos Chapter: Freeze	Weverse Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392350be1e03508a5dc.png
TXT	The Chaos Chapter: Freeze	Weverse Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392350d9ea0af8ab2fc.png
TXT	The Chaos Chapter: Freeze	Weverse Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392350f7c4f93038d39.png
TXT	The Chaos Chapter: Freeze	Target Exclusive Group Card	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db556d0020129a0374.png
TXT	The Chaos Chapter: Freeze	Withfans 2.0 Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239b5447a4f95ec06.png
TXT	The Chaos Chapter: Freeze	Withfans 2.0 Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239b3c67e56409dba.png
TXT	The Chaos Chapter: Freeze	Withfans 2.0 Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239b6c689a3051ee2.png
TXT	The Chaos Chapter: Freeze	Withfans 2.0 Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239b8681d5f0cb7f3.png
TXT	The Chaos Chapter: Freeze	Withfans 2.0 Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239ba01e29164a8ec.png
TXT	The Chaos Chapter: Freeze	Apple Music Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db48a300344bd199be.png
TXT	The Chaos Chapter: Freeze	Apple Music Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639235136b5c63a24de0.png
TXT	The Chaos Chapter: Freeze	Apple Music Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639235166f654a1ed6be.png
TXT	The Chaos Chapter: Freeze	Apple Music Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923518026df8f3ee21.png
TXT	The Chaos Chapter: Freeze	Apple Music Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392351999af6b8abf34.png
TXT	The Chaos Chapter: Freeze	Weverse Japan Preorder Group Card	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db11910012f4fc5e39.png
TXT	The Chaos Chapter: Freeze	Withfans 3.0 Online Fansign	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbb1e2001476efdbf8.png
TXT	The Chaos Chapter: Freeze	Withfans 3.0 Online Fansign	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f5eb159de27848fa.png
TXT	The Chaos Chapter: Freeze	Withfans 3.0 Online Fansign	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbb3040022ec9d3dcf.png
TXT	The Chaos Chapter: Freeze	Withfans 3.0 Online Fansign	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbb0530030cc99cdd6.png
TXT	The Chaos Chapter: Freeze	Withfans 3.0 Online Fansign	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbb3610038b4e50e1e.png
TXT	The Chaos Chapter: Freeze	Naver Shopping Live Special Event	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db58fb002f0505cc0e.png
TXT	The Chaos Chapter: Freeze	Naver Shopping Live Special Event	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239a8d768663518a9.png
TXT	The Chaos Chapter: Freeze	Naver Shopping Live Special Event	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239ac4f52508be286.png
TXT	The Chaos Chapter: Freeze	Naver Shopping Live Special Event	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db599000065f07c732.png
TXT	The Chaos Chapter: Freeze	Naver Shopping Live Special Event	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239b01c60344598b7.png
TXT	The Chaos Chapter: Freeze	Soundwave 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db41d4000a41120c97.png
TXT	The Chaos Chapter: Freeze	Soundwave 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392caf9d40c046cdec5.png
TXT	The Chaos Chapter: Freeze	Soundwave 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cafc8bf2260bae1c.png
TXT	The Chaos Chapter: Freeze	Soundwave 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cafdf0a4c739743a.png
TXT	The Chaos Chapter: Freeze	Soundwave 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67eb203b00023eb300ac.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Soobin A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dcea9e0019cfcbdb93.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Soobin B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dceabf002175155560.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Yeonjun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dceadf0023e74fd617.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Yeonjun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dceaf9003afce4992a.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Beomgyu A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dcedea000dfe73b531.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Beomgyu B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dceb3f0037a39aa27a.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Taehyun A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dce142001353c634fb.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Taehyun B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dce5fb0019ccd8bdf0.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Huening Kai A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dceb7700239a8d479a.png
TXT	The Chaos Chapter: Freeze	Universal Music Japan Lucky Draw	Huening Kai B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dceb8e0035bc5216fa.png
TXT	The Chaos Chapter: Freeze	M2U 2.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbdae3000c47f5178e.png
TXT	The Chaos Chapter: Freeze	M2U 2.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbdc2500268eb28fc6.png
TXT	The Chaos Chapter: Freeze	M2U 2.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbdc73000740fc9517.png
TXT	The Chaos Chapter: Freeze	M2U 2.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dcde870038255168c8.png
TXT	The Chaos Chapter: Freeze	M2U 2.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbdcc50033a095540d.png
TXT	The Chaos Chapter: Freeze	M2U 2.0 Lucky Draw	Group Postcard	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db1d77003b5aa3b6c0.png
TXT	The Chaos Chapter: Freeze	You Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923539a39b27c00621.png
TXT	The Chaos Chapter: Freeze	You Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923537ac9f88ccae24.png
TXT	The Chaos Chapter: Freeze	You Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392353b55f002942e03.png
TXT	The Chaos Chapter: Freeze	You Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392353cdb1606101a45.png
TXT	The Chaos Chapter: Freeze	You Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392353e816010c786e0.png
TXT	The Chaos Chapter: Freeze	Powerstation 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f5389ef792493611.png
TXT	The Chaos Chapter: Freeze	Powerstation 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f523e4f26db6a643.png
TXT	The Chaos Chapter: Freeze	Powerstation 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f548ed462567e47e.png
TXT	The Chaos Chapter: Freeze	Powerstation 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f55a1e7cb22c144b.png
TXT	The Chaos Chapter: Freeze	Powerstation 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f56d73a621dc59ac.png
TXT	The Chaos Chapter: Freeze	Original Story Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392351f47a7b05e9531.png
TXT	The Chaos Chapter: Freeze	Original Story Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c4152600104c6550e4.png
TXT	The Chaos Chapter: Freeze	Original Story Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639235210cb249918bcb.png
TXT	The Chaos Chapter: Freeze	Original Story Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923522e8aa13f2e9bb.png
TXT	The Chaos Chapter: Freeze	Original Story Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63923524bc31ff6b5cae.png
TXT	The Chaos Chapter: Freeze	Withfans 1.0 Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db6095001c14fa1a02.png
TXT	The Chaos Chapter: Freeze	Withfans 1.0 Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db613b003be913684a.png
TXT	The Chaos Chapter: Freeze	Withfans 1.0 Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db5f9a001606a73f83.png
TXT	The Chaos Chapter: Freeze	Withfans 1.0 Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db622d000e0d662c60.png
TXT	The Chaos Chapter: Freeze	Withfans 1.0 Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db628f0007c9d605de.png
TXT	The Chaos Chapter: Freeze	YES24 Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db47b60005ec13c6d2.png
TXT	The Chaos Chapter: Freeze	YES24 Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f658d668e60bea7d.png
TXT	The Chaos Chapter: Freeze	YES24 Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db47e70034336d97a5.png
TXT	The Chaos Chapter: Freeze	YES24 Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66db480c002e7a82665c.png
TXT	The Chaos Chapter: Freeze	YES24 Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f683577bbafa8106.png
TXT	The Chaos Chapter: Freeze	Lazada Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbaaf0001256bfd9c3.png
TXT	The Chaos Chapter: Freeze	Lazada Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbab130021705e423d.png
TXT	The Chaos Chapter: Freeze	Lazada Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dbabed00312b7c56b0.png
TXT	The Chaos Chapter: Freeze	Lazada Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239bd4afb232acd95.png
TXT	The Chaos Chapter: Freeze	Lazada Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639239bf30aeb735e77c.png
TXT	The Chaos Chapter: Freeze	World Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392352859e609570e47.png
TXT	The Chaos Chapter: Freeze	World Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392352687eb47158aca.png
TXT	The Chaos Chapter: Freeze	World Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392352a4074c0c376bf.png
TXT	The Chaos Chapter: Freeze	World Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392352bef02c8af8c0c.png
TXT	The Chaos Chapter: Freeze	World Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392352da69aa920647d.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave 2023 Reissue Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df4496002a376a85c3.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave 2023 Reissue Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df6af7002ca7fc1187.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave 2023 Reissue Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df6b7a001991912bd8.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave 2023 Reissue Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df6bc60026f6f0db1c.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave 2023 Reissue Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df6c770011f178dee1.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave 2023 Reissue Lucky Draw	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df6ce7001c79c74bf3.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Soobin Polaroid	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd48c3002c0febf66c.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Soobin Clear Card	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd4d9c002ea97a2c2a.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Yeonjun Polaroid	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd4ae2001abfaab40b.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Yeonjun Clear Card	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd4c1f0008022df078.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Beomgyu Polaroid	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63924372da4afb548b1b.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Beomgyu Clear Card	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd4ed3001003e0c5d7.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Taehyun Polaroid	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243747a86b525e78c.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Taehyun Clear Card	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd4f9c001c4c336ac4.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Huening Kai Polaroid	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd4989001ead7c4222.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Japan Preorder	Huening Kai Clear Card	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd504c003673eaea43.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c52d0000173068519e.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392430ac87775d62b58.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392430e34329bb08cc6.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392430fcad2c64ca06a.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243113894907fff32.png
TXT	The Chaos Chapter: Fight Or Escape	OS Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392432298bd1a448dbe.png
TXT	The Chaos Chapter: Fight Or Escape	OS Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c52cad00372f2ebe88.png
TXT	The Chaos Chapter: Fight Or Escape	OS Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392432419c4c3f81689.png
TXT	The Chaos Chapter: Fight Or Escape	OS Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243259ae04e63aa28.png
TXT	The Chaos Chapter: Fight Or Escape	OS Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243273b353fab5315.png
TXT	The Chaos Chapter: Fight Or Escape	Escape Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67362222000278ce7808.png
TXT	The Chaos Chapter: Fight Or Escape	Escape Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6735cdd3000511b35ca6.png
TXT	The Chaos Chapter: Fight Or Escape	Escape Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673622950024b80b4e66.png
TXT	The Chaos Chapter: Fight Or Escape	Escape Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673621bc0026aafb99e0.png
TXT	The Chaos Chapter: Fight Or Escape	Escape Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67362cab001ee9be6e22.png
TXT	The Chaos Chapter: Fight Or Escape	Fight AR Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5361d0019aea650d8.png
TXT	The Chaos Chapter: Fight Or Escape	Fight AR Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c533440017676a0b61.png
TXT	The Chaos Chapter: Fight Or Escape	Fight AR Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c533f3003708ade565.png
TXT	The Chaos Chapter: Fight Or Escape	Fight AR Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c52da9000e8d7fae26.png
TXT	The Chaos Chapter: Fight Or Escape	Fight AR Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5331f002e8a10e405.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Together Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639242fa26d9a45597c9.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Together Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639242f8bf998185e2f0.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Together Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639242fba57676d18847.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Together Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639242fd3adfd4cd08d3.png
TXT	The Chaos Chapter: Fight Or Escape	Fight Together Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639242feb6071e83ef99.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave Lucky Draw	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392434f367feadbef48.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave Lucky Draw	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392434d8ad26b9370b4.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave Lucky Draw	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63924350c1e77b26ca7f.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave Lucky Draw	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243524c0066129f92.png
TXT	The Chaos Chapter: Fight Or Escape	Soundwave Lucky Draw	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63924353c4b07229f0a4.png
TXT	The Chaos Chapter: Fight Or Escape	Apple Music Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ddf474002b13a45e5e.png
TXT	The Chaos Chapter: Fight Or Escape	Apple Music Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ddf501003173630b28.png
TXT	The Chaos Chapter: Fight Or Escape	Apple Music Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64187044b489a49c676f.png
TXT	The Chaos Chapter: Fight Or Escape	Apple Music Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ddf587001ecf0f58f1.png
TXT	The Chaos Chapter: Fight Or Escape	Apple Music Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6415b2d0824025c60d9f.png
TXT	The Chaos Chapter: Fight Or Escape	Apple Music Preorder	Group Stickers	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ddf3d80020657d68ed.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243778b311dfc5635.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Soobin Wappen	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd436d00090c013c64.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63924376154e6cdc2ed6.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Yeonjun Wappen	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd3ee9002cd2ad147b.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392437914ab4f88cee0.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Beomgyu Wappen	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd438200387eb9ef5d.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392437aa1662c8f18b0.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Taehyun Wappen	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd43ad003165ecdf5d.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392437c14df928957cb.png
TXT	The Chaos Chapter: Fight Or Escape	Weverse Global Preorder	Huening Kai Wappen	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd43c0001aabf43c05.png
TXT	The Chaos Chapter: Fight Or Escape	Interpark Preorder	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ea0d48be17a6f713.png
TXT	The Chaos Chapter: Fight Or Escape	Interpark Preorder	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ea00026432da948e.png
TXT	The Chaos Chapter: Fight Or Escape	Interpark Preorder	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ea187882cf0850e5.png
TXT	The Chaos Chapter: Fight Or Escape	Interpark Preorder	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ea291cc9730890d8.png
TXT	The Chaos Chapter: Fight Or Escape	Interpark Preorder	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd465d0036abe8323e.png
TXT	The Chaos Chapter: Fight Or Escape	M2U Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63924356d699756c692a.png
TXT	The Chaos Chapter: Fight Or Escape	M2U Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd445f0039be7520d8.png
TXT	The Chaos Chapter: Fight Or Escape	M2U Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243588aa8c74441fa.png
TXT	The Chaos Chapter: Fight Or Escape	M2U Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392435a0d9ed20edf7a.png
TXT	The Chaos Chapter: Fight Or Escape	M2U Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392435b7cd9c3eba56f.png
TXT	The Chaos Chapter: Fight Or Escape	Lazada Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392436580b885ce5be7.png
TXT	The Chaos Chapter: Fight Or Escape	Lazada Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639243642ad9ee699d37.png
TXT	The Chaos Chapter: Fight Or Escape	Lazada Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd3091001b95257140.png
TXT	The Chaos Chapter: Fight Or Escape	Lazada Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dd454200279c1dd631.png
TXT	The Chaos Chapter: Fight Or Escape	Lazada Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392436a2ed3de179551.png
TXT	The Chaos Chapter: Fight Or Escape	Music Korea Preorder	Soobin Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66de05cd00002c89785a.png
TXT	The Chaos Chapter: Fight Or Escape	Music Korea Preorder	Yeonjun Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66de085e001400db26ac.png
TXT	The Chaos Chapter: Fight Or Escape	Music Korea Preorder	Beomgyu Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66de07330032b079b661.png
TXT	The Chaos Chapter: Fight Or Escape	Music Korea Preorder	Taehyun Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639281c51aae0c88188d.png
TXT	The Chaos Chapter: Fight Or Escape	Music Korea Preorder	Huening Kai Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66de0786001bb907edae.png
TXT	The Chaos Chapter: Fight Or Escape	Universal Music Japan Preorder	Soobin Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737435e00017ef46c03.png
TXT	The Chaos Chapter: Fight Or Escape	Universal Music Japan Preorder	Yeonjun Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67373f87000ca65e21b3.png
TXT	The Chaos Chapter: Fight Or Escape	Universal Music Japan Preorder	Beomgyu Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67374a95000907d8883c.png
TXT	The Chaos Chapter: Fight Or Escape	Universal Music Japan Preorder	Taehyun Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67374162003b3cd2ee99.png
TXT	The Chaos Chapter: Fight Or Escape	Universal Music Japan Preorder	Huening Kai Clear Card	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6736397300318f5e2123.png
TXT	The Chaos Chapter: Fight Or Escape	Withfans 2.0 Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df3ecc000f94234a1f.png
TXT	The Chaos Chapter: Fight Or Escape	Withfans 2.0 Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df3df300227ee8dc3d.png
TXT	The Chaos Chapter: Fight Or Escape	Withfans 2.0 Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df3e6a001973097d71.png
TXT	The Chaos Chapter: Fight Or Escape	Withfans 2.0 Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df3f0e001fe1d740c6.png
TXT	The Chaos Chapter: Fight Or Escape	Withfans 2.0 Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eb059057adf51bc6.png
TXT	The Chaos Chapter: Fight Or Escape	Hybe Insight Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df406c003c66e78f74.png
TXT	The Chaos Chapter: Fight Or Escape	Hybe Insight Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df40a10024ba30081f.png
TXT	The Chaos Chapter: Fight Or Escape	Hybe Insight Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df40e80027e8a61066.png
TXT	The Chaos Chapter: Fight Or Escape	Hybe Insight Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df40c200183236aa43.png
TXT	The Chaos Chapter: Fight Or Escape	Hybe Insight Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df4111003a397d41b9.png
TXT	Chaotic Wonderland	Standard Set	Yeonjun & Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c556c00027dccd11f1.png
TXT	Chaotic Wonderland	Standard Set	Yeonjun & Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdfe5211cf1094c62b.png
TXT	Chaotic Wonderland	Standard Set	Soobin & Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdfe0fc517ff7f8370.png
TXT	Chaotic Wonderland	Standard Set	Soobin & Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdfe253f03b5ea3091.png
TXT	Chaotic Wonderland	Standard Set	Beomgyu & Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdfdf59a123472fd71.png
TXT	Chaotic Wonderland	Universal Music Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdffa007d0a5c41ae2.png
TXT	Chaotic Wonderland	Universal Music Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5552900369e698218.png
TXT	Chaotic Wonderland	Universal Music Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdffba48403c24ac87.png
TXT	Chaotic Wonderland	Universal Music Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdffca1e93f25af8b2.png
TXT	Chaotic Wonderland	Universal Music Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63bdffd6734726aa953c.png
TXT	Chaotic Wonderland	Weverse Global Preorder Group Lenticular Standee	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df991400042eb462f0.png
TXT	Chaotic Wonderland	Weverse Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfcf05002fa24aeacd.png
TXT	Chaotic Wonderland	Weverse Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfcdb300172710c620.png
TXT	Chaotic Wonderland	Weverse Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfcddc002e988522f9.png
TXT	Chaotic Wonderland	Weverse Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfce000015f598c136.png
TXT	Chaotic Wonderland	Weverse Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfce25001e28536f40.png
TXT	Chaotic Wonderland	All Stores Preorder Group Postcard	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66df82310012a77cef56.png
TXT	Chaotic Wonderland	Weverse Japan Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63be001d49bf2356a536.png
TXT	Chaotic Wonderland	Weverse Japan Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639298f72bd23279daae.png
TXT	Chaotic Wonderland	Weverse Japan Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63be002dbb00d66182da.png
TXT	Chaotic Wonderland	Weverse Japan Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639298fa112eef3a5aee.png
TXT	Chaotic Wonderland	Weverse Japan Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/639298fb862eda730c5b.png
TXT	Chaotic Wonderland	Tower Records Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfad85001f9d28e5c9.png
TXT	Chaotic Wonderland	Tower Records Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfaf6a00226aaff9a1.png
TXT	Chaotic Wonderland	Tower Records Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfb03d0016e13c9b32.png
TXT	Chaotic Wonderland	Tower Records Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfaff1001c1780f979.png
TXT	Chaotic Wonderland	Tower Records Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dfad4c0001fdc5663c.png
TXT	Minisode 2: Thursday's Child	Hate Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673773ce002f5d1b713d.png
TXT	Minisode 2: Thursday's Child	Hate Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673778f600061fd211d5.png
TXT	Minisode 2: Thursday's Child	Hate Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5595300241aaf6f9e.png
TXT	Minisode 2: Thursday's Child	Hate Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737760900219d050a84.png
TXT	Minisode 2: Thursday's Child	Hate Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c559a8002f39cb2ddb.png
TXT	Minisode 2: Thursday's Child	Mess Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2db34986182b602.png
TXT	Minisode 2: Thursday's Child	Mess Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2d9d755a9aef94a.png
TXT	Minisode 2: Thursday's Child	Mess Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c55c4f00275c8efc4b.png
TXT	Minisode 2: Thursday's Child	Mess Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2de1b99019fd0a9.png
TXT	Minisode 2: Thursday's Child	Mess Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2df9bac9f4294b1.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Soobin A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e39a63001d69fc89f8.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Soobin B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e39aac00328651cdc7.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Yeonjun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e38b4e00135b6e33cb.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Yeonjun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a545001d44e0b5d8.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Beomgyu A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a11d000e2c8254d1.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Beomgyu B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a1540005349ff58f.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Taehyun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a1c1000b3729e426.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Taehyun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a4b800074271faec.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Huening Kai A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a2950036a52ff71b.png
TXT	Minisode 2: Thursday's Child	Withfans 3.0 Online Fansign	Huening Kai B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a3c100243970cebd.png
TXT	Minisode 2: Thursday's Child	M2U 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef016d024152ba11.png
TXT	Minisode 2: Thursday's Child	M2U 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392eeffdfa183f619a1.png
TXT	Minisode 2: Thursday's Child	M2U 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef0307b831a879c4.png
TXT	Minisode 2: Thursday's Child	M2U 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef04a0845959c3b2.png
TXT	Minisode 2: Thursday's Child	M2U 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392efa19a46e853b58c.png
TXT	Minisode 2: Thursday's Child	M2U 1.0 Lucky Draw	Group Photocard	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67376fbd001defd89b5f.png
TXT	Minisode 2: Thursday's Child	Synnara Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ec352a57563ebdd1.png
TXT	Minisode 2: Thursday's Child	Synnara Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ec33e2430ea30b46.png
TXT	Minisode 2: Thursday's Child	Synnara Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ec368072cfb72a4a.png
TXT	Minisode 2: Thursday's Child	Synnara Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ec37c34dea4f2fb9.png
TXT	Minisode 2: Thursday's Child	Synnara Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ec39a144542f33f8.png
TXT	Minisode 2: Thursday's Child	Synnara Preorder	Group Sticker	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e34943003b05d7c615.png
TXT	Minisode 2: Thursday's Child	Weverse Global Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392eef620030cf79a9c.png
TXT	Minisode 2: Thursday's Child	Weverse Global Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d78e440f1b8cd8d8.png
TXT	Minisode 2: Thursday's Child	Weverse Global Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392eef8114d8b531748.png
TXT	Minisode 2: Thursday's Child	Weverse Global Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392eefa096d57ef406d.png
TXT	Minisode 2: Thursday's Child	Weverse Global Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392eefbccef9bab2acf.png
TXT	Minisode 2: Thursday's Child	Weverse Global Preorder	Group Postcard	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67376eb5003cf1a8eaa4.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef78cad86e17d13b.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef775f162b6e19d5.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef7a6351be99bf4a.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef7bf310869605c8.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef7d7165f4b86f5d.png
TXT	Minisode 2: Thursday's Child	Powerstation 2.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392efa587202cf80162.png
TXT	Minisode 2: Thursday's Child	Powerstation 2.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392efa3852d6ada1af0.png
TXT	Minisode 2: Thursday's Child	Powerstation 2.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392efa779282eecbe52.png
TXT	Minisode 2: Thursday's Child	Powerstation 2.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392efa966e324c82c88.png
TXT	Minisode 2: Thursday's Child	Powerstation 2.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392efab1814f0cd4eb2.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Soobin A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e39aed002ccf5114d2.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Soobin B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e39025000979f09164.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Yeonjun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e38a42000d9605346a.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Yeonjun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e38d9a000731b45a85.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Beomgyu A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e394b0002c26dc6133.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Beomgyu B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3999900234bb124a4.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Taehyun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e397440016993efb35.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Taehyun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e390940036bf8b3fc7.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Huening Kai A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e396e100366ac6a8dc.png
TXT	Minisode 2: Thursday's Child	Withfans 1.0 Online Fansign	Huening Kai B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e392d1003a9724f7d5.png
TXT	Minisode 2: Thursday's Child	Hybe Insight Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef1d5d5c62995bf1.png
TXT	Minisode 2: Thursday's Child	Hybe Insight Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef1bab88851420c8.png
TXT	Minisode 2: Thursday's Child	Hybe Insight Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef1f146b7c024554.png
TXT	Minisode 2: Thursday's Child	Hybe Insight Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef20bb90f4b4cf54.png
TXT	Minisode 2: Thursday's Child	Hybe Insight Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef2289b62b59f261.png
TXT	Minisode 2: Thursday's Child	Weverse Tear Ver. Preorder Postcards	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a71b002070b35560.png
TXT	Minisode 2: Thursday's Child	Weverse Tear Ver. Preorder Postcards	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a72e0014c153680b.png
TXT	Minisode 2: Thursday's Child	Weverse Tear Ver. Preorder Postcards	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a74200032b8decfb.png
TXT	Minisode 2: Thursday's Child	Weverse Tear Ver. Preorder Postcards	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a7550014c156ef87.png
TXT	Minisode 2: Thursday's Child	Weverse Tear Ver. Preorder Postcards	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e3a766001a5b1c506c.png
TXT	Minisode 2: Thursday's Child	Hate Lenticular Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cca3b5e166f9a138.png
TXT	Minisode 2: Thursday's Child	Hate Lenticular Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cca26c4fb64d7988.png
TXT	Minisode 2: Thursday's Child	Hate Lenticular Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cca51a8cf16b7263.png
TXT	Minisode 2: Thursday's Child	Hate Lenticular Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cca66ee2dccdaff8.png
TXT	Minisode 2: Thursday's Child	Hate Lenticular Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392cca7d83114110e91.png
TXT	Minisode 2: Thursday's Child	End Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c55b010015bf29e2c5.png
TXT	Minisode 2: Thursday's Child	End Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c55aee00362f933c9d.png
TXT	Minisode 2: Thursday's Child	End Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c55b1e0013a2919eb4.png
TXT	Minisode 2: Thursday's Child	End Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2d6d3dcf85c03b7.png
TXT	Minisode 2: Thursday's Child	End Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2d85b69d94d5e11.png
TXT	Minisode 2: Thursday's Child	M2U 2.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e367e3001b73c65bc5.png
TXT	Minisode 2: Thursday's Child	M2U 2.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef981a611326841a.png
TXT	Minisode 2: Thursday's Child	M2U 2.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef9c7f2c842621eb.png
TXT	Minisode 2: Thursday's Child	M2U 2.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef9e3976c423d7d8.png
TXT	Minisode 2: Thursday's Child	M2U 2.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef9fd409b002ae34.png
TXT	Minisode 2: Thursday's Child	Universal Music Japan Lucky Draw	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef80636731117ac5.png
TXT	Minisode 2: Thursday's Child	Universal Music Japan Lucky Draw	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef7f056364dd8687.png
TXT	Minisode 2: Thursday's Child	Universal Music Japan Lucky Draw	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef81e386dd1a25d2.png
TXT	Minisode 2: Thursday's Child	Universal Music Japan Lucky Draw	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef8361ec928cc4ca.png
TXT	Minisode 2: Thursday's Child	Universal Music Japan Lucky Draw	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef84cc9ce3bb7b27.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Tear Ver. Preorder	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef7207bb5214987e.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Tear Ver. Preorder	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef70bc092d5976b2.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Tear Ver. Preorder	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef736f103079d3b9.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Tear Ver. Preorder	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef74cc420ebd237e.png
TXT	Minisode 2: Thursday's Child	Weverse x Naver Live Tear Ver. Preorder	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392ef761345daf93dba.png
TXT	Minisode 2: Thursday's Child	End Lenticular Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2cd6c23d47114fc.png
TXT	Minisode 2: Thursday's Child	End Lenticular Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c55bb1002d185efddf.png
TXT	Minisode 2: Thursday's Child	End Lenticular Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2cec5846a9a547a.png
TXT	Minisode 2: Thursday's Child	End Lenticular Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2d03593518829b4.png
TXT	Minisode 2: Thursday's Child	End Lenticular Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2d19bf27f99b2bf.png
TXT	Minisode 2: Thursday's Child	End Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2c6a0a470740ea3.png
TXT	Minisode 2: Thursday's Child	End Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2c5543a9e45c7da.png
TXT	Minisode 2: Thursday's Child	End Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2c7dc15f4e0d84d.png
TXT	Minisode 2: Thursday's Child	End Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fbee58002255293a6e.png
TXT	Minisode 2: Thursday's Child	End Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2caa48e4cba3945.png
TXT	Minisode 2: Thursday's Child	Mess Lenticular Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2e29a8d23f63d7a.png
TXT	Minisode 2: Thursday's Child	Mess Lenticular Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2e12eb9ffe988ca.png
TXT	Minisode 2: Thursday's Child	Mess Lenticular Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2e400f06d9e2c78.png
TXT	Minisode 2: Thursday's Child	Mess Lenticular Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6392d2e5728daf23b832.png
TXT	Minisode 2: Thursday's Child	Mess Lenticular Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c55e2e00226e971185.png
TXT	Good Boy Gone Bad	Regular Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ec2e041111c9ed97.png
TXT	Good Boy Gone Bad	Regular Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c563c7000fc708a1e2.png
TXT	Good Boy Gone Bad	Regular Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ec3b985ff75d37a6.png
TXT	Good Boy Gone Bad	Regular Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ec46cc20b653c59f.png
TXT	Good Boy Gone Bad	Regular Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ec52103fb6f440aa.png
TXT	Good Boy Gone Bad	Limited B Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5659900282c3066ed.png
TXT	Good Boy Gone Bad	Limited B Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ed28ac70d5301520.png
TXT	Good Boy Gone Bad	Limited B Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ed3fde8142234c0b.png
TXT	Good Boy Gone Bad	Limited B Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ed4b80e594d429d4.png
TXT	Good Boy Gone Bad	Limited B Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c565ae003793fa5e37.png
TXT	Good Boy Gone Bad	HMV Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f3f19a6c73430be4.png
TXT	Good Boy Gone Bad	HMV Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f3e2e1d1bbf64bdc.png
TXT	Good Boy Gone Bad	HMV Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f3ff699d65b25196.png
TXT	Good Boy Gone Bad	HMV Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f40a7613f3e47771.png
TXT	Good Boy Gone Bad	HMV Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f4189c4a3a7825de.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Soobin A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eee78d61671ed0ed.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Soobin B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eef21a5155aa952b.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Yeonjun A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eed07c8fe858c048.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Yeonjun B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eedbbd28bb7ddb33.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Beomgyu A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5669d002702a21032.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Beomgyu B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ee584b3482e3f6c4.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Taehyun A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eefeb933246c3599.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Taehyun B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ef0be9dce494d613.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Huening Kai A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ef209fb4802277bc.png
TXT	Good Boy Gone Bad	Solo Jackets Set	Huening Kai B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1ef2e7814574b64b5.png
TXT	Good Boy Gone Bad	Uuniversal Music Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1eff9e61e5f072fbe.png
TXT	Good Boy Gone Bad	Uuniversal Music Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1efedba0f22f49e30.png
TXT	Good Boy Gone Bad	Uuniversal Music Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f003d39e1f8f1637.png
TXT	Good Boy Gone Bad	Uuniversal Music Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f00f52e236be7853.png
TXT	Good Boy Gone Bad	Uuniversal Music Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64187213c8e30fc61227.png
TXT	Good Boy Gone Bad	Osaka Venue Limited Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e79e200034eb073b45.png
TXT	Good Boy Gone Bad	Osaka Venue Limited Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7a203002dc17b499f.png
TXT	Good Boy Gone Bad	Osaka Venue Limited Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e79ecc002b383c76ae.png
TXT	Good Boy Gone Bad	Osaka Venue Limited Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7a0f70002cad13e25.png
TXT	Good Boy Gone Bad	Osaka Venue Limited Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e79fb50002146fdd68.png
TXT	Good Boy Gone Bad	Weverse Unit Set	Soobin & Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c584660008cb7ec2b7.png
TXT	Good Boy Gone Bad	Weverse Unit Set	Soobin & Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58497002c0f0bc6fc.png
TXT	Good Boy Gone Bad	Weverse Unit Set	Yeonjun & Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c584b4001287c40c41.png
TXT	Good Boy Gone Bad	Weverse Unit Set	Yeonjun & Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c585060006a65a61f7.png
TXT	Good Boy Gone Bad	Weverse Unit Set	Beomgyu & Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58535003963652613.png
TXT	Good Boy Gone Bad	Weverse Japan Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5ebb1000772e3e8d1.png
TXT	Good Boy Gone Bad	Weverse Japan Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5eb380003804797bc.png
TXT	Good Boy Gone Bad	Weverse Japan Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5ed45002975cbf57a.png
TXT	Good Boy Gone Bad	Weverse Japan Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5fe8b0027bff80039.png
TXT	Good Boy Gone Bad	Weverse Japan Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5ebfc000209f2d684.png
TXT	Good Boy Gone Bad	Weverse Japan Preorder	Group Postcard and Mount	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e4c3a60000d57485bc.png
TXT	Good Boy Gone Bad	Tower Records Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76d58002091367f5a.png
TXT	Good Boy Gone Bad	Tower Records Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76c5c00338be0cd38.png
TXT	Good Boy Gone Bad	Tower Records Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f3622712978d9221.png
TXT	Good Boy Gone Bad	Tower Records Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76fef0021914ea2d2.png
TXT	Good Boy Gone Bad	Tower Records Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76e9c0006c43f1c8b.png
TXT	Good Boy Gone Bad	Weverse Clear Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58988003a032bfb3d.png
TXT	Good Boy Gone Bad	Weverse Clear Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c589b8000e3c7de5b6.png
TXT	Good Boy Gone Bad	Weverse Clear Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c589dd001bf76101ff.png
TXT	Good Boy Gone Bad	Weverse Clear Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58a05002bad8eb288.png
TXT	Good Boy Gone Bad	Weverse Clear Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58a46003082f345d0.png
TXT	Good Boy Gone Bad	Limited A Set	Soobin & Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c57ff6002eda4f6f5f.png
TXT	Good Boy Gone Bad	Limited A Set	Soobin & Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58070003894c8bca0.png
TXT	Good Boy Gone Bad	Limited A Set	Yeonjun & Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5802a00050865ae61.png
TXT	Good Boy Gone Bad	Limited A Set	Beomgyu & Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c580ba001ab4d83e74.png
TXT	Good Boy Gone Bad	Limited A Set	Taehyun & Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c580ff00187e3b46a4.png
TXT	Good Boy Gone Bad	Weverse Global Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76098001b084ee90a.png
TXT	Good Boy Gone Bad	Weverse Global Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e760b90006800b0690.png
TXT	Good Boy Gone Bad	Weverse Global Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e760fd000d76573505.png
TXT	Good Boy Gone Bad	Weverse Global Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7614e000c4fc5787e.png
TXT	Good Boy Gone Bad	Weverse Global Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e761b20001f12eca78.png
TXT	Good Boy Gone Bad	Weverse Global Preorder	Group Lenticular Postcard	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76b66000407de282a.png
TXT	Good Boy Gone Bad	Universal Music Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77a3200209dcd3d4d.png
TXT	Good Boy Gone Bad	Universal Music Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77ac6001f5d72d805.png
TXT	Good Boy Gone Bad	Universal Music Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e777e200383b0d1dd5.png
TXT	Good Boy Gone Bad	Universal Music Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7785700025c9ab162.png
TXT	Good Boy Gone Bad	Universal Music Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77c910031dc08216a.png
TXT	Good Boy Gone Bad	All Stores Preorder Group Postcard	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e4d6f0000ac9f69f00.png
TXT	Good Boy Gone Bad	Target Exclusive	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7bc080001ffe55b00.png
TXT	Good Boy Gone Bad	Makuhari Venue Limited Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e79cd0002cddb50525.png
TXT	Good Boy Gone Bad	Makuhari Venue Limited Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e784760009dd738aa0.png
TXT	Good Boy Gone Bad	Makuhari Venue Limited Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e799680035019cbef2.png
TXT	Good Boy Gone Bad	Makuhari Venue Limited Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e786ae0006054d9b09.png
TXT	Good Boy Gone Bad	Makuhari Venue Limited Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e78f6f0009fccdb1f9.png
TXT	Good Boy Gone Bad	Tower Records Flyer Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7354b0019ec555db6.png
TXT	Good Boy Gone Bad	Tower Records Flyer Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e759670004966d2579.png
TXT	Good Boy Gone Bad	Tower Records Flyer Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e736ba0023d317ddaf.png
TXT	Good Boy Gone Bad	Tower Records Flyer Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e757d400313771e47e.png
TXT	Good Boy Gone Bad	Tower Records Flyer Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e735e30004cac525e0.png
TXT	Good Boy Gone Bad	Weverse Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77ed70027c5e39075.png
TXT	Good Boy Gone Bad	Weverse Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77d28000d2bddb56c.png
TXT	Good Boy Gone Bad	Weverse Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77637000ef8cdf686.png
TXT	Good Boy Gone Bad	Weverse Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77551003ba8f9e97f.png
TXT	Good Boy Gone Bad	Weverse Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e77da1000aa2990381.png
TXT	Good Boy Gone Bad	Universal Music Japan Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5ef4d002247ac4f96.png
TXT	Good Boy Gone Bad	Universal Music Japan Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5efe9000014964526.png
TXT	Good Boy Gone Bad	Universal Music Japan Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5f0310025fa7518b9.png
TXT	Good Boy Gone Bad	Universal Music Japan Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5f0a5000b474367be.png
TXT	Good Boy Gone Bad	Universal Music Japan Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e5f0750002b181380e.png
TXT	Good Boy Gone Bad	Japan Pop Up Store Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e76664001f6a282315.png
TXT	Good Boy Gone Bad	Japan Pop Up Store Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f3022c4c3fa465d7.png
TXT	Good Boy Gone Bad	Japan Pop Up Store Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f30ce104e16386fd.png
TXT	Good Boy Gone Bad	Japan Pop Up Store Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7678d002e44ef6b92.png
TXT	Good Boy Gone Bad	Japan Pop Up Store Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63c1f3182d3c6271ca54.png
TXT	The Name Chapter: Temptation	Daydream Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb8f6404c7c5eb2d04.png
TXT	The Name Chapter: Temptation	Daydream Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb8f8c8f1506da827b.png
TXT	The Name Chapter: Temptation	Daydream Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb8f9da7aaa1d20559.png
TXT	The Name Chapter: Temptation	Daydream Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58dbf001a6e9ec7ad.png
TXT	The Name Chapter: Temptation	Daydream Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb8fc0924efdaef759.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live Lullaby Ver. Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557d327ec35c2afe99.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live Lullaby Ver. Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557d1009779e52df02.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live Lullaby Ver. Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557d42d3484140a0f7.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live Lullaby Ver. Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea60710035adf0bda9.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live Lullaby Ver. Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557d6abe13b52dd4fe.png
TXT	The Name Chapter: Temptation	Shopee Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641a2b81ec81cec99586.png
TXT	The Name Chapter: Temptation	Shopee Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea93f5000f5d2ac2f1.png
TXT	The Name Chapter: Temptation	Shopee Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/641ecde1573eb9721f47.png
TXT	The Name Chapter: Temptation	Shopee Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea942b0025d0e21974.png
TXT	The Name Chapter: Temptation	Shopee Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea944e00162a5814e1.png
TXT	The Name Chapter: Temptation	Powerstation 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f4a015c6ce668076.png
TXT	The Name Chapter: Temptation	Powerstation 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f498aa905b144c66.png
TXT	The Name Chapter: Temptation	Powerstation 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f4a7124fbb9d31eb.png
TXT	The Name Chapter: Temptation	Powerstation 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f4af1ccf704f567a.png
TXT	The Name Chapter: Temptation	Powerstation 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f4b82f781a359960.png
TXT	The Name Chapter: Temptation	Soundwave 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f100c6f4426aeebf.png
TXT	The Name Chapter: Temptation	Soundwave 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f0f91fa28dd1c2ee.png
TXT	The Name Chapter: Temptation	Soundwave 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f11855d78a79ab07.png
TXT	The Name Chapter: Temptation	Soundwave 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f125595d14bed3bb.png
TXT	The Name Chapter: Temptation	Soundwave 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1324f273c3b9564.png
TXT	The Name Chapter: Temptation	M2U 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1bce27193a6047a.png
TXT	The Name Chapter: Temptation	M2U 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1d7675a941ed567.png
TXT	The Name Chapter: Temptation	M2U 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1de4cbce9e73043.png
TXT	The Name Chapter: Temptation	M2U 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1e639fa40525e9d.png
TXT	The Name Chapter: Temptation	M2U 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1ed0229ddc84641.png
TXT	The Name Chapter: Temptation	Weverse Japan Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645571f544dd88eecfcd.png
TXT	The Name Chapter: Temptation	Weverse Japan Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea335c000426174a33.png
TXT	The Name Chapter: Temptation	Weverse Japan Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557269da426a247dbd.png
TXT	The Name Chapter: Temptation	Weverse Japan Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645572c8db5bbbce9125.png
TXT	The Name Chapter: Temptation	Weverse Japan Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557245def0c646de53.png
TXT	The Name Chapter: Temptation	Weverse Japan Preorder	Group Tapestry	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea2ae0002b6b0c9035.png
TXT	The Name Chapter: Temptation	Nightmare Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e7241c906bed958ae.png
TXT	The Name Chapter: Temptation	Nightmare Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e725055ba01191a02.png
TXT	The Name Chapter: Temptation	Nightmare Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e729e08da5cb73183.png
TXT	The Name Chapter: Temptation	Nightmare Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e726e568d1183a36e.png
TXT	The Name Chapter: Temptation	Nightmare Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7c3d300214851511f.png
TXT	The Name Chapter: Temptation	Namil 2.0 Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f21101959598e0b1.png
TXT	The Name Chapter: Temptation	Namil 2.0 Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f1ff7474353a5193.png
TXT	The Name Chapter: Temptation	Namil 2.0 Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f228e0cfd5dda8dd.png
TXT	The Name Chapter: Temptation	Namil 2.0 Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f23f1086e647b33d.png
TXT	The Name Chapter: Temptation	Namil 2.0 Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f256269c0007945f.png
TXT	The Name Chapter: Temptation	Target Exclusive	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645635dd504e6012058f.png
TXT	The Name Chapter: Temptation	Target Exclusive	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6456386aa30954910762.png
TXT	The Name Chapter: Temptation	Target Exclusive	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6456388407e31fc5eff9.png
TXT	The Name Chapter: Temptation	Target Exclusive	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6456367fc9de09314064.png
TXT	The Name Chapter: Temptation	Target Exclusive	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea9362003163ec1481.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live 2.0 Lucky Draw	Soobin & Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea62b50020957e0c96.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live 2.0 Lucky Draw	Soobin & Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454fdec8aabf6f85c17.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live 2.0 Lucky Draw	Yeonjun & Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454fe27ae56b827d633.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live 2.0 Lucky Draw	Beomgyu & Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454fdf5c7897aff204a.png
TXT	The Name Chapter: Temptation	Weverse x Naver Live 2.0 Lucky Draw	Taehyun & Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645519405e9e344e9a6d.png
TXT	The Name Chapter: Temptation	Music Korea Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645633b79b0c3a229bec.png
TXT	The Name Chapter: Temptation	Music Korea Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645633a2c45256664e25.png
TXT	The Name Chapter: Temptation	Music Korea Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66eaa4a6002a71db02f8.png
TXT	The Name Chapter: Temptation	Music Korea Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea91e700332d247b9c.png
TXT	The Name Chapter: Temptation	Music Korea Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea917e000c5d1bd924.png
TXT	The Name Chapter: Temptation	Music Korea Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66eaa49a001c7ce0a467.png
TXT	The Name Chapter: Temptation	Dear My Muse 1.0 Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dd6972d492fbc460.png
TXT	The Name Chapter: Temptation	Dear My Muse 1.0 Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea648d00068bbeda70.png
TXT	The Name Chapter: Temptation	Dear My Muse 1.0 Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dd8233b7da76d85d.png
TXT	The Name Chapter: Temptation	Dear My Muse 1.0 Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea64b60019fabd3f31.png
TXT	The Name Chapter: Temptation	Dear My Muse 1.0 Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e3180521dfbc14d3.png
TXT	The Name Chapter: Temptation	Hottracks Preorder Postcard	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea7a4b001f9b95fe24.png
TXT	The Name Chapter: Temptation	Hottracks Preorder Postcard	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea7a6b0028b45ff51f.png
TXT	The Name Chapter: Temptation	Hottracks Preorder Postcard	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea7a9a0011046415f7.png
TXT	The Name Chapter: Temptation	Hottracks Preorder Postcard	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea7a78001d57a0a108.png
TXT	The Name Chapter: Temptation	Hottracks Preorder Postcard	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea7a3c002291ed91a4.png
TXT	The Name Chapter: Temptation	Hottracks Preorder Postcard	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea7a7f0011008eff8a.png
TXT	The Name Chapter: Temptation	Ktown4u Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de4d9e60d201654e.png
TXT	The Name Chapter: Temptation	Ktown4u Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de3d4461ce4913eb.png
TXT	The Name Chapter: Temptation	Ktown4u Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de55dc952e29abc7.png
TXT	The Name Chapter: Temptation	Ktown4u Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de73e27b82541713.png
TXT	The Name Chapter: Temptation	Ktown4u Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de7b09b589a3681e.png
TXT	The Name Chapter: Temptation	Ktown4u Preorder	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea92bc0008c38f4afe.png
TXT	The Name Chapter: Temptation	Daydream Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e761e0c36eacaf687.png
TXT	The Name Chapter: Temptation	Daydream Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e75a2baaf0289bdad.png
TXT	The Name Chapter: Temptation	Daydream Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c59013000611aae5d9.png
TXT	The Name Chapter: Temptation	Daydream Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c59061000c5988ba1b.png
TXT	The Name Chapter: Temptation	Daydream Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e75da9d2cf44013ab.png
TXT	The Name Chapter: Temptation	Dear My Muse 2.0 Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dde0be9aa9a3d461.png
TXT	The Name Chapter: Temptation	Dear My Muse 2.0 Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ddc202b4010a9da0.png
TXT	The Name Chapter: Temptation	Dear My Muse 2.0 Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ddf89a9ea67cbb39.png
TXT	The Name Chapter: Temptation	Dear My Muse 2.0 Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de0e30f62c59d4b6.png
TXT	The Name Chapter: Temptation	Dear My Muse 2.0 Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454de23a034c954564e.png
TXT	The Name Chapter: Temptation	Namil 1.0 Online Fansign	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f38aa39b56a02139.png
TXT	The Name Chapter: Temptation	Namil 1.0 Online Fansign	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f36ed3a7af095641.png
TXT	The Name Chapter: Temptation	Namil 1.0 Online Fansign	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f39f4404e76c56b4.png
TXT	The Name Chapter: Temptation	Namil 1.0 Online Fansign	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f5ded4523c403486.png
TXT	The Name Chapter: Temptation	Namil 1.0 Online Fansign	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f3c3c6f8d76e1c9f.png
TXT	The Name Chapter: Temptation	Soundwave 2.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e269d73980681c90.png
TXT	The Name Chapter: Temptation	Soundwave 2.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e298e08b824e709e.png
TXT	The Name Chapter: Temptation	Soundwave 2.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e27151ece8cbb8fc.png
TXT	The Name Chapter: Temptation	Soundwave 2.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e27be270e3338060.png
TXT	The Name Chapter: Temptation	Soundwave 2.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737c207003dff5a90f7.png
TXT	The Name Chapter: Temptation	Weverse Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e07c69bbf3c899e2.png
TXT	The Name Chapter: Temptation	Weverse Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e0693a42fac43bf3.png
TXT	The Name Chapter: Temptation	Weverse Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e0a211515c83777d.png
TXT	The Name Chapter: Temptation	Weverse Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e0a8e7c3c905e0f9.png
TXT	The Name Chapter: Temptation	Weverse Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e0b221211a02891b.png
TXT	The Name Chapter: Temptation	Farewell Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e6d6ddbdcc9b19bcb.png
TXT	The Name Chapter: Temptation	Farewell Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e6d7cc8150c625c5f.png
TXT	The Name Chapter: Temptation	Farewell Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e6d8f6bbcb9b86094.png
TXT	The Name Chapter: Temptation	Farewell Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e6d9e15a4687aa295.png
TXT	The Name Chapter: Temptation	Farewell Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c593bd00047f33372e.png
TXT	The Name Chapter: Temptation	Aladin Preorder Clear Postcard	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557eb5306dd2d0328f.png
TXT	The Name Chapter: Temptation	Aladin Preorder Clear Postcard	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557e9dc275c01f9fd0.png
TXT	The Name Chapter: Temptation	Aladin Preorder Clear Postcard	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557ed32772459ae2f7.png
TXT	The Name Chapter: Temptation	Aladin Preorder Clear Postcard	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557f3104771b5d71a7.png
TXT	The Name Chapter: Temptation	Aladin Preorder Clear Postcard	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557f465d75a1760dca.png
TXT	The Name Chapter: Temptation	Aladin Preorder Clear Postcard	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e90816001137057be1.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e719042ea7b85738.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e726104b7193acc6.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e72d713dfdb4262c.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e734765fb635abff.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454e73b411db90edcf6.png
TXT	The Name Chapter: Temptation	Musicplant Preorder	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645579723ddce2fd5576.png
TXT	The Name Chapter: Temptation	Musicplant Preorder	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645577df54a82a70bf99.png
TXT	The Name Chapter: Temptation	Musicplant Preorder	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6455798a44a23c336e09.png
TXT	The Name Chapter: Temptation	Musicplant Preorder	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6455799db1b73252f731.png
TXT	The Name Chapter: Temptation	Musicplant Preorder	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e8c9480009bb63c809.png
TXT	The Name Chapter: Temptation	Musicplant Preorder	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645579d2930f1931c414.png
TXT	The Name Chapter: Temptation	Nightmare Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb95694138e5e501e7.png
TXT	The Name Chapter: Temptation	Nightmare Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb9575e2607ab0ab97.png
TXT	The Name Chapter: Temptation	Nightmare Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58e2f003195423605.png
TXT	The Name Chapter: Temptation	Nightmare Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c58e4c00044a5d5580.png
TXT	The Name Chapter: Temptation	Nightmare Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb959f9b919ef301ff.png
TXT	The Name Chapter: Temptation	Synnara Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ebf1691941ef4694.png
TXT	The Name Chapter: Temptation	Synnara Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ebe9d2bbd7a4d080.png
TXT	The Name Chapter: Temptation	Synnara Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea5ef8001c13f6bd31.png
TXT	The Name Chapter: Temptation	Synnara Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ebff3598afb29d6f.png
TXT	The Name Chapter: Temptation	Synnara Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ec1838339b2f9013.png
TXT	The Name Chapter: Temptation	Synnara Preorder	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454ec1ea3b93092289e.png
TXT	The Name Chapter: Temptation	Weverse Light Back Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbe6e46b5ffdc7d1e.png
TXT	The Name Chapter: Temptation	Weverse Light Back Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c595a10003729d5484.png
TXT	The Name Chapter: Temptation	Weverse Light Back Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbe7f5b744b9d27be.png
TXT	The Name Chapter: Temptation	Weverse Light Back Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbe960c6fd14437d1.png
TXT	The Name Chapter: Temptation	Weverse Light Back Set	Hueningkai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbea3dc7c8382455a.png
TXT	The Name Chapter: Temptation	Yes24 Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dc517fdf0e3dc6a1.png
TXT	The Name Chapter: Temptation	Yes24 Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dc44c97c21f2ce90.png
TXT	The Name Chapter: Temptation	Yes24 Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dc58bfdb365e93d8.png
TXT	The Name Chapter: Temptation	Yes24 Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dc5fe0209929da27.png
TXT	The Name Chapter: Temptation	Yes24 Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dc9103f21864a084.png
TXT	The Name Chapter: Temptation	Yes24 Preorder	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454dc6f23a3366df57f.png
TXT	The Name Chapter: Temptation	Lullaby Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fba7f612724c08ea45.png
TXT	The Name Chapter: Temptation	Lullaby Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fba7dcd08cbae6a3b1.png
TXT	The Name Chapter: Temptation	Lullaby Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5945f000eb52697a0.png
TXT	The Name Chapter: Temptation	Lullaby Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fba8132d1e047eb30c.png
TXT	The Name Chapter: Temptation	Lullaby Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fba8215bb63329804f.png
TXT	The Name Chapter: Temptation	Universal Music Japan Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557211ce1382333681.png
TXT	The Name Chapter: Temptation	Universal Music Japan Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645574f334bcb9206d84.png
TXT	The Name Chapter: Temptation	Universal Music Japan Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6455752bc2dba5898132.png
TXT	The Name Chapter: Temptation	Universal Music Japan Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6455747561590c79cc59.png
TXT	The Name Chapter: Temptation	Universal Music Japan Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6455745fbaa92c63e97f.png
TXT	The Name Chapter: Temptation	Universal Music Japan Preorder	Group Clear Poster	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ea3b3b0010fee19fbc.png
TXT	The Name Chapter: Temptation	Lullaby Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e780c1af1357eb025.png
TXT	The Name Chapter: Temptation	Lullaby Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e77fdc3ddff77e675.png
TXT	The Name Chapter: Temptation	Lullaby Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e78188b0c3938cf82.png
TXT	The Name Chapter: Temptation	Lullaby Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e7826cb2cc8ce5241.png
TXT	The Name Chapter: Temptation	Lullaby Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/648e78319db2068b6a65.png
TXT	The Name Chapter: Temptation	Farewell Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb9aacf108feba1387.png
TXT	The Name Chapter: Temptation	Farewell Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb9aba151da0f32986.png
TXT	The Name Chapter: Temptation	Farewell Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb9ac7b8044de97d06.png
TXT	The Name Chapter: Temptation	Farewell Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb9ad62a0a23150f99.png
TXT	The Name Chapter: Temptation	Farewell Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fb9ae4c8686c05464e.png
TXT	The Name Chapter: Temptation	Weverse Dark Back Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbb95cb623f688cd38.png
TXT	The Name Chapter: Temptation	Weverse Dark Back Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c594c00006826b7389.png
TXT	The Name Chapter: Temptation	Weverse Dark Back Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbb32f364d8e19606.png
TXT	The Name Chapter: Temptation	Weverse Dark Back Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbbd15e3b220aa9ec.png
TXT	The Name Chapter: Temptation	Weverse Dark Back Set	Hueningkai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/63fbbc7b8287500e3615.png
TXT	The Name Chapter: Temptation	Powerstation 2.0 Lucky Draw	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f7dab896b9a9e4fb.png
TXT	The Name Chapter: Temptation	Powerstation 2.0 Lucky Draw	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f7d479c78252fb30.png
TXT	The Name Chapter: Temptation	Powerstation 2.0 Lucky Draw	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f7e17e64c4f54c73.png
TXT	The Name Chapter: Temptation	Powerstation 2.0 Lucky Draw	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f7e7d7b1ab07d18b.png
TXT	The Name Chapter: Temptation	Powerstation 2.0 Lucky Draw	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6454f7eebcfd85119335.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lullaby Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645577161fdf0b010714.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lullaby Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557706d67197915fa0.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lullaby Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6455772e2aa163c7d2e5.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lullaby Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/64557743168e0feb2c52.png
TXT	The Name Chapter: Temptation	Universal Music Japan Lullaby Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/645577574fa887606fc6.png
TXT	Sweet	Limited A Set	Yeonjun & Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a19c00027adecf77.png
TXT	Sweet	Limited A Set	Beomgyu & Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66aead91002bf8d03025.png
TXT	Sweet	Limited A Set	Taehyun & Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a2280031faa769de.png
TXT	Sweet	Limited B Set	Soobin & Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a3e1002ee9958027.png
TXT	Sweet	Limited B Set	Soobin & Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a40100279e579359.png
TXT	Sweet	Limited B Set	Yeonjun & Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a3af001b510bafe1.png
TXT	Sweet	Limited B Set	Yeonjun & Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66aead2400160e7aeb30.png
TXT	Sweet	Limited B Set	Beomgyu & Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a4260006b6bdc041.png
TXT	Sweet	Weverse Japan Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c63c010029bcce0108.png
TXT	Sweet	Weverse Japan Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c63bbe00302e5efa93.png
TXT	Sweet	Weverse Japan Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c63c5500318ec6245c.png
TXT	Sweet	Weverse Japan Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c63ca600148bde5005.png
TXT	Sweet	Weverse Japan Set	Taehyun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c63dee003adf42de5c.png
TXT	Sweet	Weverse Japan Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c63cdf000828148ae4.png
TXT	Sweet	Universal Music Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a57e0014bfc48663.png
TXT	Sweet	Universal Music Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a5b7002f5f77fa06.png
TXT	Sweet	Universal Music Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a65a000d8ab4d5ce.png
TXT	Sweet	Universal Music Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a60a0002ddcd3472.png
TXT	Sweet	Universal Music Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a633000af726cffc.png
TXT	Sweet	7netshopping Selfie Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a760003e4da8e790.png
TXT	Sweet	7netshopping Selfie Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a79e0008e84451ef.png
TXT	Sweet	7netshopping Selfie Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a8070007a15337e3.png
TXT	Sweet	7netshopping Selfie Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a836002501f04457.png
TXT	Sweet	7netshopping Selfie Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c5a85900310c5c2e0b.png
TXT	Sweet	HMV Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf9070000df0e0be7.png
TXT	Sweet	HMV Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf94d00016260a51c.png
TXT	Sweet	HMV Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf9f0001290759046.png
TXT	Sweet	HMV Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edfb00001fd5574186.png
TXT	Sweet	HMV Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edfb6f0018816bfbc1.png
TXT	Sweet	Weverse Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf46b002ea8d86ba8.png
TXT	Sweet	Weverse Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf3db00077d3a4036.png
TXT	Sweet	Weverse Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf4c4003509e743ec.png
TXT	Sweet	Weverse Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf519000e67c60cdd.png
TXT	Sweet	Weverse Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edf5ba0035d09a845f.png
TXT	Sweet	ACT:SWEET MIRAGE x Weverse Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb5840028e8857ea7.png
TXT	Sweet	ACT:SWEET MIRAGE x Weverse Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb5ac0002f9b54ed8.png
TXT	Sweet	ACT:SWEET MIRAGE x Weverse Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb65e0004f20e0ff2.png
TXT	Sweet	ACT:SWEET MIRAGE x Weverse Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb6090005fb6e150a.png
TXT	Sweet	ACT:SWEET MIRAGE x Weverse Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb633003912f0d1cf.png
TXT	Sweet	Weverse Global Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecad48002fb2af3ca4.png
TXT	Sweet	Weverse Global Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecadc5000e94ad5a08.png
TXT	Sweet	Weverse Global Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecae26002b0a48b159.png
TXT	Sweet	Weverse Global Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecae5b00073e9c86ac.png
TXT	Sweet	Weverse Global Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecae9d00099363a249.png
TXT	Sweet	Weverse Global Preorder	Group Mini Poster	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecb59f00228e6f7b10.png
TXT	Sweet	Weverse Japan Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecbd78001e01000a29.png
TXT	Sweet	Weverse Japan Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecbd4f002f4ba40ed8.png
TXT	Sweet	Weverse Japan Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecbd01000a3c728ab0.png
TXT	Sweet	Weverse Japan Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecbc87001cad6dbc23.png
TXT	Sweet	Weverse Japan Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecbcc600140ab0edab.png
TXT	Sweet	Weverse Japan Preorder	Group Bromide	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee74100037b62e2eff.png
TXT	Sweet	Tower Records Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edfc0a00314f036fbd.png
TXT	Sweet	Tower Records Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edfc500018c3e55273.png
TXT	Sweet	Tower Records Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edfdc50010508ba560.png
TXT	Sweet	Tower Records Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66edffa10020b88a5476.png
TXT	Sweet	Tower Records Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee014d002657972e17.png
TXT	Sweet	Universal Music Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee05a300202f38a480.png
TXT	Sweet	Universal Music Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee05ee000a1ec61a45.png
TXT	Sweet	Universal Music Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee06a80032c017d5d1.png
TXT	Sweet	Universal Music Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee078100213a6ff3c6.png
TXT	Sweet	Universal Music Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee06fb002b953040c4.png
TXT	Sweet	ACT:SWEET MIRAGE x Universal Music Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efa9fb000fa847b694.png
TXT	Sweet	ACT:SWEET MIRAGE x Universal Music Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efac3500356d8050d5.png
TXT	Sweet	ACT:SWEET MIRAGE x Universal Music Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efaff9003c5fedd11a.png
TXT	Sweet	ACT:SWEET MIRAGE x Universal Music Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb1fe001fba87fd19.png
TXT	Sweet	ACT:SWEET MIRAGE x Universal Music Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66efb2db001517268b36.png
TXT	Sweet	Target Exclusive Group Card	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ecb213002ec4389930.png
TXT	Sweet	HMV Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef5fcb001536b021f1.png
TXT	Sweet	HMV Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef618f000c5d858e86.png
TXT	Sweet	HMV Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef5e5600226c709ce5.png
TXT	Sweet	HMV Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee6eb900216cce3db6.png
TXT	Sweet	HMV Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ee75f6002248d85068.png
TXT	Sweet	Tower Records Shibuya Exclusive Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef8b60002861f34ef4.png
TXT	Sweet	Tower Records Shibuya Exclusive Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef8c800036d1a2e310.png
TXT	Sweet	Tower Records Shibuya Exclusive Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef8d0f0023a0dda661.png
TXT	Sweet	Tower Records Shibuya Exclusive Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef8ad200002dd2a870.png
TXT	Sweet	Tower Records Shibuya Exclusive Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef9d2a000413f26f97.png
TXT	Sweet	Tower Records Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef93b80031be374e08.png
TXT	Sweet	Tower Records Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef98c5003686283f06.png
TXT	Sweet	Tower Records Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef97f6000a7b6116e6.png
TXT	Sweet	Tower Records Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef973d001aa6e04d17.png
TXT	Sweet	Tower Records Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ef956b000ef3298856.png
TXT	The Name Chapter: Freefall	CU Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c78000234aaea324.png
TXT	The Name Chapter: Freefall	CU Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c760000eaa5b7c9a.png
TXT	The Name Chapter: Freefall	CU Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c7c90018ef779e7f.png
TXT	The Name Chapter: Freefall	CU Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c8280013b431ef31.png
TXT	The Name Chapter: Freefall	CU Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c86200384975725e.png
TXT	The Name Chapter: Freefall	Dear My Muse Online Fansign	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8b71b000642af580a.png
TXT	The Name Chapter: Freefall	Dear My Muse Online Fansign	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8b76c0000d7ed9e79.png
TXT	The Name Chapter: Freefall	Dear My Muse Online Fansign	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8b7d900081d3d37c6.png
TXT	The Name Chapter: Freefall	Dear My Muse Online Fansign	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8b82a00319a3dc8ff.png
TXT	The Name Chapter: Freefall	Dear My Muse Online Fansign	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8b853001d736eaa6d.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Showcase	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8cd63000f8ed9bff9.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Showcase	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8d3e20036cff861f4.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Showcase	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8d41a001c70c0d8f8.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Showcase	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8d47000070012ba24.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Showcase	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8d4a900073866ef87.png
TXT	The Name Chapter: Freefall	Weverse Japan 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89b53003743d356fe.png
TXT	The Name Chapter: Freefall	Weverse Japan 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89ba80009a3edbd73.png
TXT	The Name Chapter: Freefall	Weverse Japan 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89bf1002bd9f87f10.png
TXT	The Name Chapter: Freefall	Weverse Japan 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89c33000b811ea953.png
TXT	The Name Chapter: Freefall	Weverse Japan 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89c83000acea51997.png
TXT	The Name Chapter: Freefall	KakaoTalk Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c37b000bbe80b85f.png
TXT	The Name Chapter: Freefall	KakaoTalk Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c4d10011a9da7bd9.png
TXT	The Name Chapter: Freefall	KakaoTalk Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c28a001cecacb457.png
TXT	The Name Chapter: Freefall	KakaoTalk Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c5380015b0a71770.png
TXT	The Name Chapter: Freefall	KakaoTalk Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8c2ea0013ace5a0c5.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Online Fansign	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8bb090010eda250a0.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Online Fansign	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8bba10002d32701e2.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Online Fansign	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8bd24000b26e61e73.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Online Fansign	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8be190030eff67469.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Online Fansign	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8be830021d7f95d49.png
TXT	The Name Chapter: Freefall	Universal Music Japan 1.0 Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89df0002c56b44a04.png
TXT	The Name Chapter: Freefall	Universal Music Japan 1.0 Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89e1600103549fa49.png
TXT	The Name Chapter: Freefall	Universal Music Japan 1.0 Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89e46002d26bb7d8c.png
TXT	The Name Chapter: Freefall	Universal Music Japan 1.0 Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89e890032e73ac67c.png
TXT	The Name Chapter: Freefall	Universal Music Japan 1.0 Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f89eb3003e19332b54.png
TXT	The Name Chapter: Freefall	Withfans 2.0 Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f87b1f00197119de6f.png
TXT	The Name Chapter: Freefall	Withfans 2.0 Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f87b7000176b03fa95.png
TXT	The Name Chapter: Freefall	Withfans 2.0 Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f87bbc003bf89eec5d.png
TXT	The Name Chapter: Freefall	Withfans 2.0 Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f87bfb001b65b1f720.png
TXT	The Name Chapter: Freefall	Withfans 2.0 Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f87c2f000b6f688d13.png
TXT	The Name Chapter: Freefall	Target Exclusive	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f88e08001e2b37fffb.png
TXT	The Name Chapter: Freefall	Target Exclusive	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f88e700015d65540cf.png
TXT	The Name Chapter: Freefall	Target Exclusive	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f88ea4001c67342055.png
TXT	The Name Chapter: Freefall	Target Exclusive	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f88ec200307e923ff2.png
TXT	The Name Chapter: Freefall	Target Exclusive	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f88eed002394a0c2bc.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f865e6000a8e48e42c.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f866040033bb306348.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f866270018f833319f.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f86654000dfde61d32.png
TXT	The Name Chapter: Freefall	Withfans 1.0 Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8668700039c5b3516.png
TXT	The Name Chapter: Freefall	Weverse Japan Gravity Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f85f970013d4ae2a3e.png
TXT	The Name Chapter: Freefall	Weverse Japan Gravity Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f860360035a0b1098b.png
TXT	The Name Chapter: Freefall	Weverse Japan Gravity Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f860720019546162ae.png
TXT	The Name Chapter: Freefall	Weverse Japan Gravity Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8609f00367eb84dd2.png
TXT	The Name Chapter: Freefall	Weverse Japan Gravity Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f861180029252982d0.png
TXT	The Name Chapter: Freefall	Weverse Japan Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b9ea002e602476e6.png
TXT	The Name Chapter: Freefall	Weverse Japan Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ba1e0027697978b6.png
TXT	The Name Chapter: Freefall	Weverse Japan Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ba4400227204f830.png
TXT	The Name Chapter: Freefall	Weverse Japan Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ba750036926144a4.png
TXT	The Name Chapter: Freefall	Weverse Japan Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ba9f002ba7c6adf3.png
TXT	The Name Chapter: Freefall	Weverse Global Weverse Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f859bc0012b832e01b.png
TXT	The Name Chapter: Freefall	Weverse Global Weverse Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f85a100022a6787a0b.png
TXT	The Name Chapter: Freefall	Weverse Global Weverse Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f85ae90028f581ff42.png
TXT	The Name Chapter: Freefall	Weverse Global Weverse Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f85b1c00353786aab2.png
TXT	The Name Chapter: Freefall	Weverse Global Weverse Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f85b52002b3fd2f9ca.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c3c000117be1f652.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Soobin Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c6a0002e7bb815f8.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c412002ae1ea0c2f.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Yeonjun Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c6d7001da94e8277.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c442000f22a5ae77.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Beomgyu Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c6540026ae960acd.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c4670034206f7328.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Taehyun Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c70a001e4ca9d861.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c48e002c58c3e665.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Huening Kai Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c73b001a2c371180.png
TXT	The Name Chapter: Freefall	Weverse Global Standard Ver. Preorder	Group Lenticular	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c5a50025512e6198.png
TXT	The Name Chapter: Freefall	Weverse Global Gravity Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8561e002e6a305d1d.png
TXT	The Name Chapter: Freefall	Weverse Global Gravity Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8564b0021249e24db.png
TXT	The Name Chapter: Freefall	Weverse Global Gravity Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8567a0026b23bd95c.png
TXT	The Name Chapter: Freefall	Weverse Global Gravity Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f856eb0032fdaa0031.png
TXT	The Name Chapter: Freefall	Weverse Global Gravity Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f8573200332c6091fd.png
TXT	The Name Chapter: Freefall	Universal Music Japan Gravity Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c0df002b86aa1ca6.png
TXT	The Name Chapter: Freefall	Universal Music Japan Gravity Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c17700070770058b.png
TXT	The Name Chapter: Freefall	Universal Music Japan Gravity Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c1000018d3a3c949.png
TXT	The Name Chapter: Freefall	Universal Music Japan Gravity Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c113001a6492fd94.png
TXT	The Name Chapter: Freefall	Universal Music Japan Gravity Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7c122003db0e0e5d8.png
TXT	The Name Chapter: Freefall	Universal Music Japan Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b8ff003ac0c2f31f.png
TXT	The Name Chapter: Freefall	Universal Music Japan Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b92e000bbef3751d.png
TXT	The Name Chapter: Freefall	Universal Music Japan Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b94f0000b514eedd.png
TXT	The Name Chapter: Freefall	Universal Music Japan Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b96b0015f766ae95.png
TXT	The Name Chapter: Freefall	Universal Music Japan Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b9940012bf6ced54.png
TXT	The Name Chapter: Freefall	Universal Music Japan Standard Ver. Preorder	Group Clear Poster	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fa10a30013a8ac30d4.png
TXT	The Name Chapter: Freefall	Sponge Music Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b1380036ca17ca0b.png
TXT	The Name Chapter: Freefall	Sponge Music Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b15b0013c9ce18fa.png
TXT	The Name Chapter: Freefall	Sponge Music Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b17e0018fbc82eaa.png
TXT	The Name Chapter: Freefall	Sponge Music Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b19f00001d18c0a1.png
TXT	The Name Chapter: Freefall	Sponge Music Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b1bb001796f215dd.png
TXT	The Name Chapter: Freefall	Sponge Music Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7b1e1003380378e15.png
TXT	The Name Chapter: Freefall	Musicplant Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ad9b0011e506f944.png
TXT	The Name Chapter: Freefall	Musicplant Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7add10005bcf170d5.png
TXT	The Name Chapter: Freefall	Musicplant Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7adf40011150cd2e8.png
TXT	The Name Chapter: Freefall	Musicplant Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ae31001dc3ea2459.png
TXT	The Name Chapter: Freefall	Musicplant Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7ae6c002d00e27d78.png
TXT	The Name Chapter: Freefall	Musicplant Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7aee7003d1ea3550d.png
TXT	The Name Chapter: Freefall	Music Korea Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a95600221ea8e0d8.png
TXT	The Name Chapter: Freefall	Music Korea Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a99b0024db085c63.png
TXT	The Name Chapter: Freefall	Music Korea Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a9fd003b80896992.png
TXT	The Name Chapter: Freefall	Music Korea Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7aa34003c3336b78f.png
TXT	The Name Chapter: Freefall	Music Korea Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7aa68000bdd20b6f5.png
TXT	The Name Chapter: Freefall	Music Korea Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a8b8001e40c0d481.png
TXT	The Name Chapter: Freefall	Blue Dream Media Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f79bfb001e31157737.png
TXT	The Name Chapter: Freefall	Blue Dream Media Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f79b7e00180e67681b.png
TXT	The Name Chapter: Freefall	Blue Dream Media Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f79c46003c462028b5.png
TXT	The Name Chapter: Freefall	Blue Dream Media Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f79c6f0023a07d9524.png
TXT	The Name Chapter: Freefall	Blue Dream Media Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f79c920005183c6653.png
TXT	The Name Chapter: Freefall	Blue Dream Media Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f79cb1002ac9591b91.png
TXT	The Name Chapter: Freefall	Ktown4u Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a544002be041cb2e.png
TXT	The Name Chapter: Freefall	Ktown4u Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a5900020444737fc.png
TXT	The Name Chapter: Freefall	Ktown4u Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a5d7001ca0d1aebc.png
TXT	The Name Chapter: Freefall	Ktown4u Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a615003df0180ca5.png
TXT	The Name Chapter: Freefall	Ktown4u Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a6510003dd7888d5.png
TXT	The Name Chapter: Freefall	Ktown4u Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7a6960007481b3d23.png
TXT	The Name Chapter: Freefall	Aladdin Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f764430015bfa3776a.png
TXT	The Name Chapter: Freefall	Aladdin Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f7636e000ae6e6e9ad.png
TXT	The Name Chapter: Freefall	Aladdin Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f76a8200161ce501e0.png
TXT	The Name Chapter: Freefall	Aladdin Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f76b630025c50d0dbc.png
TXT	The Name Chapter: Freefall	Aladdin Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f76baf0002ef8f34a4.png
TXT	The Name Chapter: Freefall	Aladdin Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f76bec0031568b968d.png
TXT	The Name Chapter: Freefall	Gravity Postcard Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6cc66003d986bb8bd.png
TXT	The Name Chapter: Freefall	Gravity Postcard Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6cc46003616df3c53.png
TXT	The Name Chapter: Freefall	Gravity Postcard Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6cc82002a1b8fd326.png
TXT	The Name Chapter: Freefall	Gravity Postcard Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6cca6002b1871815f.png
TXT	The Name Chapter: Freefall	Gravity Postcard Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6ccc3002112b82144.png
TXT	The Name Chapter: Freefall	Gravity Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65ac003707ef39e621af.png
TXT	The Name Chapter: Freefall	Gravity Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65299134edbaee40e46f.png
TXT	The Name Chapter: Freefall	Gravity Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65ac0089cc0c3d57a7a0.png
TXT	The Name Chapter: Freefall	Gravity Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65299146dbf21cbbfd45.png
TXT	The Name Chapter: Freefall	Gravity Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65299159946fd299d13e.png
TXT	The Name Chapter: Freefall	Weverse B Set	Soobin A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c5fc000a0e1712c6.png
TXT	The Name Chapter: Freefall	Weverse B Set	Soobin B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c647001795fb9c19.png
TXT	The Name Chapter: Freefall	Weverse B Set	Yeonjun A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c5600039446f22db.png
TXT	The Name Chapter: Freefall	Weverse B Set	Yeonjun B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c58f00308564cfae.png
TXT	The Name Chapter: Freefall	Weverse B Set	Beomgyu A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c680003cf1bcc767.png
TXT	The Name Chapter: Freefall	Weverse B Set	Beomgyu B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c6cb0008e4727dba.png
TXT	The Name Chapter: Freefall	Weverse B Set	Taehyun A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c6fa000a77e803ad.png
TXT	The Name Chapter: Freefall	Weverse B Set	Taehyun B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c733003700280bea.png
TXT	The Name Chapter: Freefall	Weverse B Set	Huening Kai A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c75b000ed27d84aa.png
TXT	The Name Chapter: Freefall	Weverse B Set	Huening Kai B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c7910019a801a030.png
TXT	The Name Chapter: Freefall	Weverse A Set	Soobin A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abfef73705cf9cba07.png
TXT	The Name Chapter: Freefall	Weverse A Set	Soobin B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff07529c7de9af17.png
TXT	The Name Chapter: Freefall	Weverse A Set	Yeonjun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff7f1ecd76b6929d.png
TXT	The Name Chapter: Freefall	Weverse A Set	Yeonjun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff8dc2e1d2de3b0c.png
TXT	The Name Chapter: Freefall	Weverse A Set	Beomgyu A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abfed2e058f9083d1b.png
TXT	The Name Chapter: Freefall	Weverse A Set	Beomgyu B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abfee60057e1655b6f.png
TXT	The Name Chapter: Freefall	Weverse A Set	Taehyun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff1e0e7723f44bdd.png
TXT	The Name Chapter: Freefall	Weverse A Set	Taehyun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff3304965a92053e.png
TXT	The Name Chapter: Freefall	Weverse A Set	Huening Kai A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff47a18a45095207.png
TXT	The Name Chapter: Freefall	Weverse A Set	Huening Kai B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65abff5cdf6756c61295.png
TXT	The Name Chapter: Freefall	QR Set	Group A	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c100001092f778a8.png
TXT	The Name Chapter: Freefall	QR Set	Group B	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c14c003a168d5edf.png
TXT	The Name Chapter: Freefall	QR Set	Group C	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6c18f001697f68428.png
TXT	The Name Chapter: Freefall	Clarity Set	Soobin A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68c85002b25a39d59.png
TXT	The Name Chapter: Freefall	Clarity Set	Soobin B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68d0b0022b8778ca2.png
TXT	The Name Chapter: Freefall	Clarity Set	Yeonjun A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68c280003a6faf2a3.png
TXT	The Name Chapter: Freefall	Clarity Set	Yeonjun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68c54001f43a6d528.png
TXT	The Name Chapter: Freefall	Clarity Set	Beomgyu A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68d3b000d12567762.png
TXT	The Name Chapter: Freefall	Clarity Set	Beomgyu B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68d7500304f4e3ed3.png
TXT	The Name Chapter: Freefall	Clarity Set	Taehyun A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68dd2002d71c103b9.png
TXT	The Name Chapter: Freefall	Clarity Set	Taehyun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c68e1400388b2c19cd.png
TXT	The Name Chapter: Freefall	Clarity Set	Huening Kai A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/652990d951eaaf8bd5a0.png
TXT	The Name Chapter: Freefall	Clarity Set	Huening Kai B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/652990ed11a94339ef4c.png
TXT	The Name Chapter: Freefall	Clarity Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6a27f001e1cb24d9b.png
TXT	The Name Chapter: Freefall	Clarity Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6a220000901a10e17.png
TXT	The Name Chapter: Freefall	Clarity Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6a2570020d888ffa0.png
TXT	The Name Chapter: Freefall	Clarity Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6a1fe001e483eff98.png
TXT	The Name Chapter: Freefall	Clarity Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6aaf80035ce6f7f07.png
TXT	The Name Chapter: Freefall	Melancholy Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6809e002032eda278.png
TXT	The Name Chapter: Freefall	Melancholy Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6807e002f132c8f34.png
TXT	The Name Chapter: Freefall	Melancholy Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c680c8001899752133.png
TXT	The Name Chapter: Freefall	Melancholy Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c680e2003525fd6941.png
TXT	The Name Chapter: Freefall	Melancholy Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6873e0034e014a36a.png
TXT	The Name Chapter: Freefall	Melancholy Set	Soobin A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c675af00082aa15d1f.png
TXT	The Name Chapter: Freefall	Melancholy Set	Soobin B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c675d8000afd16c3e7.png
TXT	The Name Chapter: Freefall	Melancholy Set	Yeonjun A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c67388003b54e2edf6.png
TXT	The Name Chapter: Freefall	Melancholy Set	Yeonjun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c67550000acc4c4393.png
TXT	The Name Chapter: Freefall	Melancholy Set	Beomgyu A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298f2bccbf0e20bdd3.png
TXT	The Name Chapter: Freefall	Melancholy Set	Beomgyu B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6761100044cf61c17.png
TXT	The Name Chapter: Freefall	Melancholy Set	Taehyun A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c67480003255cd72ae.png
TXT	The Name Chapter: Freefall	Melancholy Set	Taehyun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c6741f002251b4204f.png
TXT	The Name Chapter: Freefall	Melancholy Set	Huening Kai A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c674be00061e2f0800.png
TXT	The Name Chapter: Freefall	Melancholy Set	Huening Kai B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c673dc002493478208.png
TXT	The Name Chapter: Freefall	Reality Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c64ef8001277932e26.png
TXT	The Name Chapter: Freefall	Reality Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c64ed50028ef53140e.png
TXT	The Name Chapter: Freefall	Reality Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c64f1c001b0e72eb41.png
TXT	The Name Chapter: Freefall	Reality Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c64f5400078477f346.png
TXT	The Name Chapter: Freefall	Reality Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c64f7400132243c186.png
TXT	The Name Chapter: Freefall	Reality Set	Soobin A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298da203745df9e739.png
TXT	The Name Chapter: Freefall	Reality Set	Soobin B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298db9db8a10c19497.png
TXT	The Name Chapter: Freefall	Reality Set	Yeonjun A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298d4e0399690c4fa8.png
TXT	The Name Chapter: Freefall	Reality Set	Yeonjun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298d8a92134bb2aa20.png
TXT	The Name Chapter: Freefall	Reality Set	Beomgyu A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298dcddaa8a523e2e1.png
TXT	The Name Chapter: Freefall	Reality Set	Beomgyu B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298de70e3b74fcb1ec.png
TXT	The Name Chapter: Freefall	Reality Set	Taehyun A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298e0934a2c0001460.png
TXT	The Name Chapter: Freefall	Reality Set	Taehyun B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298e45540a910b5bf9.png
TXT	The Name Chapter: Freefall	Reality Set	Huening Kai A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/65298e5b9441b2691719.png
TXT	The Name Chapter: Freefall	Reality Set	Huening Kai B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c649390028c7634303.png
TXT	Minisode 3: Tomorrow	Ethereal Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1b208000b7a2a4c81.png
TXT	Minisode 3: Tomorrow	Ethereal Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1b1a4002f72bf1e41.png
TXT	Minisode 3: Tomorrow	Ethereal Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1b24b003182570026.png
TXT	Minisode 3: Tomorrow	Ethereal Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1b2b90004e54d9ec7.png
TXT	Minisode 3: Tomorrow	Ethereal Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1a4f3001ca2d9650c.png
TXT	Minisode 3: Tomorrow	Romantic Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f8f100380ff6c452.png
TXT	Minisode 3: Tomorrow	Romantic Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f8a1003e5fffacb7.png
TXT	Minisode 3: Tomorrow	Romantic Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f93b0024e0ceacb4.png
TXT	Minisode 3: Tomorrow	Romantic Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f977002628e8d390.png
TXT	Minisode 3: Tomorrow	Romantic Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f9ba002722987136.png
TXT	Minisode 3: Tomorrow	Ethereal Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f202f600187f555230.png
TXT	Minisode 3: Tomorrow	Ethereal Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f78e002b819f4e44.png
TXT	Minisode 3: Tomorrow	Ethereal Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f7db000c9c384a52.png
TXT	Minisode 3: Tomorrow	Ethereal Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f7fc001fcd875121.png
TXT	Minisode 3: Tomorrow	Ethereal Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f81d002d4e854337.png
TXT	Minisode 3: Tomorrow	Romantic Postcard Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fa43002682a155be.png
TXT	Minisode 3: Tomorrow	Romantic Postcard Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1f9da0016970a063c.png
TXT	Minisode 3: Tomorrow	Romantic Postcard Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fa16000c32b7c896.png
TXT	Minisode 3: Tomorrow	Romantic Postcard Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fa7100241e322129.png
TXT	Minisode 3: Tomorrow	Romantic Postcard Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fa320026a0efa360.png
TXT	Minisode 3: Tomorrow	Promise Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fd540024c6e0b779.png
TXT	Minisode 3: Tomorrow	Promise Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fd8a001d0a306a59.png
TXT	Minisode 3: Tomorrow	Promise Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fbfe000f677d85b5.png
TXT	Minisode 3: Tomorrow	Promise Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fd6c003802f71847.png
TXT	Minisode 3: Tomorrow	Promise Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fdde002f4c379c83.png
TXT	Minisode 3: Tomorrow	Promise Postcard Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1febd003bd8b35f29.png
TXT	Minisode 3: Tomorrow	Promise Postcard Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c86a0d003a6deeeb2c.png
TXT	Minisode 3: Tomorrow	Promise Postcard Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fe79000b4c4db1e2.png
TXT	Minisode 3: Tomorrow	Promise Postcard Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66dcd7650030af333b50.png
TXT	Minisode 3: Tomorrow	Promise Postcard Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1fe3100139c37587d.png
TXT	Minisode 3: Tomorrow	Light Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1ff80000bb834d260.png
TXT	Minisode 3: Tomorrow	Light Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66b03d560012e19232bf.png
TXT	Minisode 3: Tomorrow	Light Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8b6700006c81b5dcc.png
TXT	Minisode 3: Tomorrow	Light Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f1ff58001a7a27238f.png
TXT	Minisode 3: Tomorrow	Light Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66aeae1f003ae026a173.png
TXT	Minisode 3: Tomorrow	Light Mini Poster Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f4958800165557ec7b.png
TXT	Minisode 3: Tomorrow	Light Mini Poster Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f49a3e00304f8380b1.png
TXT	Minisode 3: Tomorrow	Light Mini Poster Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f49a5c0033e07a0272.png
TXT	Minisode 3: Tomorrow	Light Mini Poster Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f49a94003306544c8c.png
TXT	Minisode 3: Tomorrow	Light Mini Poster Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f49ab5003d33c8df98.png
TXT	Minisode 3: Tomorrow	Weverse A Set A	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f465180007f42aa954.png
TXT	Minisode 3: Tomorrow	Weverse A Set A	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20bdc002b43f52bf5.png
TXT	Minisode 3: Tomorrow	Weverse A Set A	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20925000f11ae05d7.png
TXT	Minisode 3: Tomorrow	Weverse A Set A	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2088f00282d24d5bf.png
TXT	Minisode 3: Tomorrow	Weverse A Set A	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f208da000b344c21de.png
TXT	Minisode 3: Tomorrow	Weverse A Set B	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20c72003d0bb0289a.png
TXT	Minisode 3: Tomorrow	Weverse A Set B	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20cdc0026e2ed43c8.png
TXT	Minisode 3: Tomorrow	Weverse A Set B	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20c350027aa0166ce.png
TXT	Minisode 3: Tomorrow	Weverse A Set B	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f465e7002c688ec5d5.png
TXT	Minisode 3: Tomorrow	Weverse A Set B	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7c968003804515ebd.png
TXT	Minisode 3: Tomorrow	Weverse A QR Set	A	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7ca1200164b186e39.png
TXT	Minisode 3: Tomorrow	Weverse A QR Set	B	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7ca58001d7b0e45da.png
TXT	Minisode 3: Tomorrow	Weverse A QR Set	C	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7cceb000df9915eef.png
TXT	Minisode 3: Tomorrow	Weverse B Set A	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20ff50037d49d582d.png
TXT	Minisode 3: Tomorrow	Weverse B Set A	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20f520017541bcecc.png
TXT	Minisode 3: Tomorrow	Weverse B Set A	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f212010018d86a384d.png
TXT	Minisode 3: Tomorrow	Weverse B Set A	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f210c50032a8e343ab.png
TXT	Minisode 3: Tomorrow	Weverse B Set A	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f211270030a9b4a856.png
TXT	Minisode 3: Tomorrow	Weverse B Set B	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f211d20033b5e11305.png
TXT	Minisode 3: Tomorrow	Weverse B Set B	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20f8d00396170ff6d.png
TXT	Minisode 3: Tomorrow	Weverse B Set B	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21063000d438842e4.png
TXT	Minisode 3: Tomorrow	Weverse B Set B	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f210f30001ba9b99b5.png
TXT	Minisode 3: Tomorrow	Weverse B Set B	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2116700051203a90a.png
TXT	Minisode 3: Tomorrow	Weverse B QR Set	A	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20707002324db2557.png
TXT	Minisode 3: Tomorrow	Weverse B QR Set	B	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20716000db4db821e.png
TXT	Minisode 3: Tomorrow	Weverse B QR Set	C	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f20724001e89a7fa37.png
TXT	Minisode 3: Tomorrow	KiT Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c89d53000f4f33c7a3.png
TXT	Minisode 3: Tomorrow	KiT Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c89dab0010fec70045.png
TXT	Minisode 3: Tomorrow	KiT Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c89c850004ee96cad6.png
TXT	Minisode 3: Tomorrow	KiT Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c89cc1003cf731f399.png
TXT	Minisode 3: Tomorrow	KiT Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c89ade00390cfcc34d.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Soobin A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a110001ebdc3ae28.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Soobin B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a13400077e62ccc3.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Yeonjun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a1eb00255360b92f.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Yeonjun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a24400203453956c.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Beomgyu A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a3ff003b1f27258b.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Beomgyu B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a412002210c51450.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Taehyun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a2ed003ba524d173.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Taehyun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a32f000f2581daee.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Huening Kai A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a024003ae8b0967b.png
TXT	Minisode 3: Tomorrow	KiT Postcard Set	Huening Kai B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8a03c000d85f053f3.png
TXT	Minisode 3: Tomorrow	Boxset Group Holo Postcard Set	Group A	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8ddc3002d3a13b9a4.png
TXT	Minisode 3: Tomorrow	Boxset Group Holo Postcard Set	Group B	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8de290010ff2ccf9e.png
TXT	Minisode 3: Tomorrow	Aladdin Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe08f70006bf376e6b.png
TXT	Minisode 3: Tomorrow	Aladdin Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe09160022a241bc16.png
TXT	Minisode 3: Tomorrow	Aladdin Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe092e00333c891e83.png
TXT	Minisode 3: Tomorrow	Aladdin Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe095000236e3789d5.png
TXT	Minisode 3: Tomorrow	Aladdin Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe09640007e14cb9cb.png
TXT	Minisode 3: Tomorrow	Aladdin Standard Ver. Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe097b0008e8053442.png
TXT	Minisode 3: Tomorrow	Aladdin Light Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67007b970038eb02cee3.png
TXT	Minisode 3: Tomorrow	Aladdin Light Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe90ab000cdada1c84.png
TXT	Minisode 3: Tomorrow	Aladdin Light Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe97c5003330cd5c7c.png
TXT	Minisode 3: Tomorrow	Aladdin Light Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe95d7002745980c7c.png
TXT	Minisode 3: Tomorrow	Aladdin Light Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe96240015361fb673.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe1706001423f56905.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe173c0034913e5fa5.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe176200049af163fe.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe179100273d02189a.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe17bc003e502283fc.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Standard Ver. Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe17e300312ea45561.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Light Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702e2210036d575ca61.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Light Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6706d23600060140b4f4.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Light Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702e25c000830184d7c.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Light Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702e2ad00129a3e4e87.png
TXT	Minisode 3: Tomorrow	Blue Dream Media Light Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702e2e300201cd275b0.png
TXT	Minisode 3: Tomorrow	KakaoTalk Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67006c8b003513d18598.png
TXT	Minisode 3: Tomorrow	KakaoTalk Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700393500015c2706b9.png
TXT	Minisode 3: Tomorrow	KakaoTalk Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a86d0005bd026f84.png
TXT	Minisode 3: Tomorrow	KakaoTalk Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67006cc400100e0ccac1.png
TXT	Minisode 3: Tomorrow	KakaoTalk Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702ed34001c650a1807.png
TXT	Minisode 3: Tomorrow	KakaoTalk Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702ecbd001c611a6dce.png
TXT	Minisode 3: Tomorrow	Ktown4u Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67007d580004367ea0ce.png
TXT	Minisode 3: Tomorrow	Ktown4u Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67002a4f001168c6ca97.png
TXT	Minisode 3: Tomorrow	Ktown4u Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a744000956ad6708.png
TXT	Minisode 3: Tomorrow	Ktown4u Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67006aee00114a667c21.png
TXT	Minisode 3: Tomorrow	Ktown4u Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67009d7e00131cc041bf.png
TXT	Minisode 3: Tomorrow	Ktown4u Standard Ver. Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe182a002e5c470389.png
TXT	Minisode 3: Tomorrow	Ktown4u Light Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67007dd200027a4c8067.png
TXT	Minisode 3: Tomorrow	Ktown4u Light Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67002a9e00278b3f3bfb.png
TXT	Minisode 3: Tomorrow	Ktown4u Light Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a7a600219ac0d3f5.png
TXT	Minisode 3: Tomorrow	Ktown4u Light Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67006b810039fe97a529.png
TXT	Minisode 3: Tomorrow	Ktown4u Light Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67009e190015fd528c9e.png
TXT	Minisode 3: Tomorrow	Music Korea Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67007b26003a97c7cc8b.png
TXT	Minisode 3: Tomorrow	Music Korea Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b405002c964a0155.png
TXT	Minisode 3: Tomorrow	Music Korea Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe9a1b002855c2fd90.png
TXT	Minisode 3: Tomorrow	Music Korea Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670066d80027c17a1578.png
TXT	Minisode 3: Tomorrow	Music Korea Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67009c910035c3b887a1.png
TXT	Minisode 3: Tomorrow	Music Korea Standard Ver. Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b453001ae5650ba6.png
TXT	Minisode 3: Tomorrow	Music Korea Light Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b5750002c0ac9719.png
TXT	Minisode 3: Tomorrow	Music Korea Light Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b595000145d58ec2.png
TXT	Minisode 3: Tomorrow	Music Korea Light Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b5c60007a77771e7.png
TXT	Minisode 3: Tomorrow	Music Korea Light Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b5f30016e1b81886.png
TXT	Minisode 3: Tomorrow	Music Korea Light Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b61f000f303d986a.png
TXT	Minisode 3: Tomorrow	Musicplant Standard Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67007a94002bf18925cd.png
TXT	Minisode 3: Tomorrow	Musicplant Standard Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670029fc001045099c90.png
TXT	Minisode 3: Tomorrow	Musicplant Standard Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a696002cf42f93d5.png
TXT	Minisode 3: Tomorrow	Musicplant Standard Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670063b8001b8b1c4203.png
TXT	Minisode 3: Tomorrow	Musicplant Standard Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67009c320004af8456c7.png
TXT	Minisode 3: Tomorrow	Musicplant Standard Ver. Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe13eb003a8c0b32b3.png
TXT	Minisode 3: Tomorrow	Musicplant Light Ver. Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b6de00237ad4ed8a.png
TXT	Minisode 3: Tomorrow	Musicplant Light Ver. Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b70c00044301b439.png
TXT	Minisode 3: Tomorrow	Musicplant Light Ver. Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe99c30001c3b7e479.png
TXT	Minisode 3: Tomorrow	Musicplant Light Ver. Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b72e001a3fe97ef5.png
TXT	Minisode 3: Tomorrow	Musicplant Light Ver. Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700b74700076f48f83e.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Standard Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702f742002cf2fe2d59.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Standard Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702fbb20035c4821bab.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Standard Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702fc2e001d1242f424.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Standard Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702f78a0027963d7013.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Standard Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702fc6600360f87f938.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Standard Ver. Preorder	Group Clear Poster	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700bdba001252985d6e.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Light Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702ffc60009feeebf49.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Light Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6702fffd0010e1e5c738.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Light Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6703003d0009d5307344.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Light Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6703007500275563790a.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Light Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6703009a0031062f1d69.png
TXT	Minisode 3: Tomorrow	Weverse Global Standard Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe109d002ee6e57c29.png
TXT	Minisode 3: Tomorrow	Weverse Global Standard Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe10d900395c5a5a58.png
TXT	Minisode 3: Tomorrow	Weverse Global Standard Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe1129000572e4d064.png
TXT	Minisode 3: Tomorrow	Weverse Global Standard Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe11a0000deebb92a8.png
TXT	Minisode 3: Tomorrow	Weverse Global Standard Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe11c7000e61ff0204.png
TXT	Minisode 3: Tomorrow	Weverse Global Standard Ver. Preorder	Group Photo Ticket	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe121500140eead7f5.png
TXT	Minisode 3: Tomorrow	Weverse Global Light Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe143a003710605d8c.png
TXT	Minisode 3: Tomorrow	Weverse Global Light Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe14690003be489c65.png
TXT	Minisode 3: Tomorrow	Weverse Global Light Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe149f0024904b9e03.png
TXT	Minisode 3: Tomorrow	Weverse Global Light Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670060a600324c03d868.png
TXT	Minisode 3: Tomorrow	Weverse Global Light Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67009226002df6bdd989.png
TXT	Minisode 3: Tomorrow	Weverse Japan Standard Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67057cf600060856a528.png
TXT	Minisode 3: Tomorrow	Weverse Japan Standard Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fef8ba001bd7e8c6f0.png
TXT	Minisode 3: Tomorrow	Weverse Japan Standard Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67057d0e0015e68a922f.png
TXT	Minisode 3: Tomorrow	Weverse Japan Standard Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67057d3d002477a11e6c.png
TXT	Minisode 3: Tomorrow	Weverse Japan Standard Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67057d230027291b1943.png
TXT	Minisode 3: Tomorrow	Weverse Japan Standard Ver. Preorder	Group Postcard	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a03f002da207f4a5.png
TXT	Minisode 3: Tomorrow	Weverse Japan Light Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700745300005a19ca07.png
TXT	Minisode 3: Tomorrow	Weverse Japan Light Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fefb66003415024062.png
TXT	Minisode 3: Tomorrow	Weverse Japan Light Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a401002e906245e6.png
TXT	Minisode 3: Tomorrow	Weverse Japan Light Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67005fe00029b98b0cb9.png
TXT	Minisode 3: Tomorrow	Weverse Japan Light Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700865b00215e1cf919.png
TXT	Minisode 3: Tomorrow	Yes24 Standard Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe98ba00283f57a4f7.png
TXT	Minisode 3: Tomorrow	Yes24 Standard Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe99320011a7ace475.png
TXT	Minisode 3: Tomorrow	Yes24 Standard Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe98f100282ad09b7f.png
TXT	Minisode 3: Tomorrow	Yes24 Standard Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700360500060b768738.png
TXT	Minisode 3: Tomorrow	Yes24 Standard Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700832e00321415302e.png
TXT	Minisode 3: Tomorrow	Yes24 Standard Ver. Preorder	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fe16a70024c57ab607.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670077c9002b25f09adc.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ff0248001348222cef.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a4f50004b4067062.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67006205002627616803.png
TXT	Minisode 3: Tomorrow	Universal Music Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670092f1002d6ea38198.png
TXT	Minisode 3: Tomorrow	Yes24 Light Ver. Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670072b9001b59f5e284.png
TXT	Minisode 3: Tomorrow	Yes24 Light Ver. Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66fef322000016a6621d.png
TXT	Minisode 3: Tomorrow	Yes24 Light Ver. Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a328001779954c7f.png
TXT	Minisode 3: Tomorrow	Yes24 Light Ver. Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/670036930004df948923.png
TXT	Minisode 3: Tomorrow	Yes24 Light Ver. Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700837700166decddae.png
TXT	Minisode 3: Tomorrow	Weverse Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705ad7800127e6c8d45.png
TXT	Minisode 3: Tomorrow	Weverse Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705adb40032faf55efc.png
TXT	Minisode 3: Tomorrow	Weverse Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705addd001008ab2115.png
TXT	Minisode 3: Tomorrow	Weverse Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705ae8b002d1cec576b.png
TXT	Minisode 3: Tomorrow	Weverse Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705aec000022569f3c4.png
TXT	Minisode 3: Tomorrow	Olive Young Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705b16d0008dfa9f815.png
TXT	Minisode 3: Tomorrow	Olive Young Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705b1d60022ce07ba60.png
TXT	Minisode 3: Tomorrow	Olive Young Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705b20f001c3c42e65e.png
TXT	Minisode 3: Tomorrow	Olive Young Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705b250001b9b43f7f3.png
TXT	Minisode 3: Tomorrow	Olive Young Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6705b29c00053509ade5.png
TXT	Minisode 3: Tomorrow	Dear My Muse 1.0 Online Fansign	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67007eac001c5f41f655.png
TXT	Minisode 3: Tomorrow	Dear My Muse 1.0 Online Fansign	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67002ca70036b850b0ec.png
TXT	Minisode 3: Tomorrow	Dear My Muse 1.0 Online Fansign	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6700a8aa003e275b3cb7.png
TXT	Minisode 3: Tomorrow	Dear My Muse 1.0 Online Fansign	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67006e92002e522a2d36.png
TXT	Minisode 3: Tomorrow	Dear My Muse 1.0 Online Fansign	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67009ed5001780b03252.png
TXT	誓い Chikai	ACT : PROMISE In Japan Nagoya Venue Limited Lucky Draw	Soobin x Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6718476e000c52562767.png
TXT	誓い Chikai	ACT : PROMISE In Japan Nagoya Venue Limited Lucky Draw	Soobin x Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184c5600027c70c628.png
TXT	誓い Chikai	ACT : PROMISE In Japan Nagoya Venue Limited Lucky Draw	Soobin x Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184c25002b812ca33f.png
TXT	誓い Chikai	ACT : PROMISE In Japan Nagoya Venue Limited Lucky Draw	Yeonjun x Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671847be00163f3ea5d2.png
TXT	誓い Chikai	ACT : PROMISE In Japan Nagoya Venue Limited Lucky Draw	Yeonjun x Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671847e7003b36bd98c0.png
TXT	誓い Chikai	ACT : PROMISE In Japan Nagoya Venue Limited Lucky Draw	Beomgyu x Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184c910011ae324b08.png
TXT	誓い Chikai	ACT : PROMISE In Japan All Venues Limited Lucky Draw	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67182589001f064bcc52.png
TXT	誓い Chikai	ACT : PROMISE In Japan All Venues Limited Lucky Draw	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671825a20024a0dd4635.png
TXT	誓い Chikai	ACT : PROMISE In Japan All Venues Limited Lucky Draw	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671825ba0010dd2dac66.png
TXT	誓い Chikai	ACT : PROMISE In Japan All Venues Limited Lucky Draw	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671825d50039a7ce3646.png
TXT	誓い Chikai	ACT : PROMISE In Japan All Venues Limited Lucky Draw	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67182856000bd590276d.png
TXT	誓い Chikai	ACT : PROMISE In Japan Osaka Venue Limited Lucky Draw	Soobin x Huening Kai A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184114000d5e6f1356.png
TXT	誓い Chikai	ACT : PROMISE In Japan Osaka Venue Limited Lucky Draw	Soobin x Huening Kai B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6718413e0013fa1dbf3e.png
TXT	誓い Chikai	ACT : PROMISE In Japan Osaka Venue Limited Lucky Draw	Yeonjun x Beomgyu A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67183a1b002f2721b287.png
TXT	誓い Chikai	ACT : PROMISE In Japan Osaka Venue Limited Lucky Draw	Yeonjun x Beomgyu B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671840b3001d063f478f.png
TXT	誓い Chikai	ACT : PROMISE In Japan Osaka Venue Limited Lucky Draw	Yeonjun x Taehyun A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671839690026a40b90fe.png
TXT	誓い Chikai	ACT : PROMISE In Japan Osaka Venue Limited Lucky Draw	Yeonjun x Taehyun B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6718406f0003b7a01fc2.png
TXT	誓い Chikai	ACT : PROMISE In Japan Tokyo Venue Limited Lucky Draw	Soobin x Beomgyu A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184e6c0006c01ba7c3.png
TXT	誓い Chikai	ACT : PROMISE In Japan Tokyo Venue Limited Lucky Draw	Soobin x Beomgyu B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671852d70009cb1bc161.png
TXT	誓い Chikai	ACT : PROMISE In Japan Tokyo Venue Limited Lucky Draw	Soobin x Taehyun A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184946001eba7b293d.png
TXT	誓い Chikai	ACT : PROMISE In Japan Tokyo Venue Limited Lucky Draw	Soobin x Taehyun B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67184b9c00226bcdbce9.png
TXT	誓い Chikai	ACT : PROMISE In Japan Tokyo Venue Limited Lucky Draw	Yeonjun x Huening Kai A	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671841af001da15c3af5.png
TXT	誓い Chikai	ACT : PROMISE In Japan Tokyo Venue Limited Lucky Draw	Yeonjun x Huening Kai B	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6718484100092ce7f143.png
TXT	誓い Chikai	Target Exclusive	Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c8143f00233d294af6.png
TXT	誓い Chikai	Odaiba Adventure King x Universal Music Japan Venue Limited Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715f3140016641a012b.png
TXT	誓い Chikai	Odaiba Adventure King x Universal Music Japan Venue Limited Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715f34c00293e921cc2.png
TXT	誓い Chikai	Odaiba Adventure King x Universal Music Japan Venue Limited Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715f37f00236e683752.png
TXT	誓い Chikai	Odaiba Adventure King x Universal Music Japan Venue Limited Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715f3b90033edf9f1cb.png
TXT	誓い Chikai	Odaiba Adventure King x Universal Music Japan Venue Limited Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715f3e70016a61b89f8.png
TXT	誓い Chikai	HMV Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671587fc0007d986caa1.png
TXT	誓い Chikai	HMV Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67159b490007499af5ef.png
TXT	誓い Chikai	HMV Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671585b6003b80fa9e38.png
TXT	誓い Chikai	HMV Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67159c7000251f30ff1b.png
TXT	誓い Chikai	HMV Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67158281002264a9c8cd.png
TXT	誓い Chikai	Tower Records Lucky Draw Flyers	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67159d53003c624a128a.png
TXT	誓い Chikai	Tower Records Lucky Draw Flyers	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67159e71000188ffbae5.png
TXT	誓い Chikai	Tower Records Lucky Draw Flyers	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715d4cb00381988b739.png
TXT	誓い Chikai	Tower Records Lucky Draw Flyers	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715d51300313b505564.png
TXT	誓い Chikai	Tower Records Lucky Draw Flyers	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715d28b00185c1672f8.png
TXT	誓い Chikai	HMV Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671574100012600c77ce.png
TXT	誓い Chikai	HMV Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671573900006a65820c9.png
TXT	誓い Chikai	HMV Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715745e002fcd945e0a.png
TXT	誓い Chikai	HMV Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fdf300340f7503dc.png
TXT	誓い Chikai	HMV Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715770a001ec75fb12b.png
TXT	誓い Chikai	Tower Records Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671566dd0029e601072c.png
TXT	誓い Chikai	Tower Records Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67156712002a0e977ed3.png
TXT	誓い Chikai	Tower Records Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671567630021e5f0cfe2.png
TXT	誓い Chikai	Tower Records Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715678f002d1c993f7d.png
TXT	誓い Chikai	Tower Records Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fd57001fd0715711.png
TXT	誓い Chikai	Universal Music Japan Lucky Draw	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671563f80006a27a95a2.png
TXT	誓い Chikai	Universal Music Japan Lucky Draw	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671561b90005ddf29056.png
TXT	誓い Chikai	Universal Music Japan Lucky Draw	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671564f9001adad318b2.png
TXT	誓い Chikai	Universal Music Japan Lucky Draw	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67156576001111dc69dd.png
TXT	誓い Chikai	Universal Music Japan Lucky Draw	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67156682001aa7f9d831.png
TXT	誓い Chikai	Weverse Japan Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67155e9f002208d251b3.png
TXT	誓い Chikai	Weverse Japan Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67155f83002d122bdfce.png
TXT	誓い Chikai	Weverse Japan Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67155edc002398958f71.png
TXT	誓い Chikai	Weverse Japan Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fdb500139a93244a.png
TXT	誓い Chikai	Weverse Japan Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fe200016e25491bf.png
TXT	誓い Chikai	All Other Stores General Preorder Group Postcard	Group Postcard	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712f77a002d71daf0c1.png
TXT	誓い Chikai	Tsutaya Preorder Group Poster	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6715432d0028a017a8c5.png
TXT	誓い Chikai	HMV Preorder Transparent Group Poster	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712e2c70024f07364e8.png
TXT	誓い Chikai	Amazon Japan Preorder Mega Jackets	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6714052c00036d26bbc0.png
TXT	誓い Chikai	Amazon Japan Preorder Mega Jackets	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67140547001d635ba20b.png
TXT	誓い Chikai	Amazon Japan Preorder Mega Jackets	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67140560000dc4b318b6.png
TXT	誓い Chikai	Amazon Japan Preorder Mega Jackets	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67140577002291db599f.png
TXT	誓い Chikai	Amazon Japan Preorder Mega Jackets	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6714058d002748b8954c.png
TXT	誓い Chikai	Amazon Japan Preorder Mega Jackets	Regular Ver.	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671405af003e72597f65.png
TXT	誓い Chikai	Tower Records Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fbca0021887f2854.png
TXT	誓い Chikai	Tower Records Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fa77002cd2292416.png
TXT	誓い Chikai	Tower Records Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fc03003a60570121.png
TXT	誓い Chikai	Tower Records Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fab7001003822837.png
TXT	誓い Chikai	Tower Records Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712fac9002565ee5c0e.png
TXT	誓い Chikai	Universal Music Japan Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671402aa00237b358b64.png
TXT	誓い Chikai	Universal Music Japan Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671402f80019033f6c00.png
TXT	誓い Chikai	Universal Music Japan Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67140339003df7fe07be.png
TXT	誓い Chikai	Universal Music Japan Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671403df0026f27350c8.png
TXT	誓い Chikai	Universal Music Japan Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67140424002d6874092c.png
TXT	誓い Chikai	Weverse Global Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6713134b003a913497bb.png
TXT	誓い Chikai	Weverse Global Preorder	Soobin Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671312a0002544263a44.png
TXT	誓い Chikai	Weverse Global Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6713144e000d623c9bbf.png
TXT	誓い Chikai	Weverse Global Preorder	Yeonjun Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671312860020f42268ba.png
TXT	誓い Chikai	Weverse Global Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671314f7000f86230ec9.png
TXT	誓い Chikai	Weverse Global Preorder	Beomgyu Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67130af2000f17e98f49.png
TXT	誓い Chikai	Weverse Global Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67131586000a33fe9a03.png
TXT	誓い Chikai	Weverse Global Preorder	Taehyun Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67131270003a4c81e993.png
TXT	誓い Chikai	Weverse Global Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/671315c0000fb9e533dc.png
TXT	誓い Chikai	Weverse Global Preorder	Huening Kai Photo Standee	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6713123b003a35a37a20.png
TXT	誓い Chikai	Weverse Global Preorder	Group Photo	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67130949000fc1a651c3.png
TXT	誓い Chikai	Weverse Japan Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712f0b2000067cfb21e.png
TXT	誓い Chikai	Weverse Japan Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712f163001e3c29e5ba.png
TXT	誓い Chikai	Weverse Japan Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712f17e002901f3406d.png
TXT	誓い Chikai	Weverse Japan Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712f19f001210a689ce.png
TXT	誓い Chikai	Weverse Japan Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6712f1b600213e137a30.png
TXT	誓い Chikai	Universal Music Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2293600161b806680.png
TXT	誓い Chikai	Universal Music Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2266e0024255cd1ac.png
TXT	誓い Chikai	Universal Music Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f22b46000ed42e8c1f.png
TXT	誓い Chikai	Universal Music Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f22b930021c34e3e76.png
TXT	誓い Chikai	Universal Music Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f229a8003d22eeddd3.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Soobin A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2341d0013f9624ca2.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Soobin B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2383d00056c6042bc.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Yeonjun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2336b002ffaff04c2.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Yeonjun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23648000b7b86be69.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Beomgyu A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f238f60012e9fdf1a8.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Beomgyu B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23581002727a29264.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Taehyun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23d45001986b5cd11.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Taehyun B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23b22003ada7ffbb5.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Huening Kai A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f235300005bd83ce6e.png
TXT	誓い Chikai	Weverse Japan Polaroid Set	Huening Kai B	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23a0c001126633db9.png
TXT	誓い Chikai	Weverse Japan Postcard Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2411b00106ecc4acc.png
TXT	誓い Chikai	Weverse Japan Postcard Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23f7e0006a596a914.png
TXT	誓い Chikai	Weverse Japan Postcard Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23d93000d4aaa08d9.png
TXT	誓い Chikai	Weverse Japan Postcard Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2404500309adfff46.png
TXT	誓い Chikai	Weverse Japan Postcard Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f23ffa0021b7fbf144.png
TXT	誓い Chikai	Weverse Japan Postcard Set	Group	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f243c1001d0e107d37.png
TXT	誓い Chikai	Solo Jacket Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f220ac001996a10ef7.png
TXT	誓い Chikai	Solo Jacket Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f220bf00342d69d39d.png
TXT	誓い Chikai	Solo Jacket Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2203700229910c06f.png
TXT	誓い Chikai	Solo Jacket Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2204a00369b37364e.png
TXT	誓い Chikai	Solo Jacket Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2205f0038c29724b7.png
TXT	誓い Chikai	Limited B Selfie Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21f6a0000cb155c92.png
TXT	誓い Chikai	Limited B Selfie Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21f8c003e644d1f35.png
TXT	誓い Chikai	Limited B Selfie Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21fc000091b686d5a.png
TXT	誓い Chikai	Limited B Selfie Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66e7d154002f3dcecfd2.png
TXT	誓い Chikai	Limited B Selfie Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66baa71d002ebb1b7f82.png
TXT	誓い Chikai	Limited A Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f2196200330b09a4ae.png
TXT	誓い Chikai	Limited A Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ba9cb00000aca955e8.png
TXT	誓い Chikai	Limited A Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21c2900029eb866d0.png
TXT	誓い Chikai	Limited A Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21a8f0010641db03b.png
TXT	誓い Chikai	Limited A Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f21aa5000b78db76eb.png
TXT	誓い Chikai	Limited A Set	Digital Code Group	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ba9add002d9f77f831.png
TXT	誓い Chikai	Standard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66ba98b0002868efcf9f.png
TXT	誓い Chikai	Standard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f215610011f60fec82.png
TXT	誓い Chikai	Standard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66f216dc00237c3bb4b2.png
TXT	誓い Chikai	Standard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66cf56fc00111642183c.png
TXT	誓い Chikai	Standard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/66c806fa001a89f09743.png
TXT	The Star Chapter: Sanctuary	Cassette Tape	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759f9460001b8839645.png
TXT	The Star Chapter: Sanctuary	Cassette Tape	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759f95500017f1d4233.png
TXT	The Star Chapter: Sanctuary	Cassette Tape	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759f9670037e6476bc5.png
TXT	The Star Chapter: Sanctuary	Cassette Tape	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759f97a001937ee5fbc.png
TXT	The Star Chapter: Sanctuary	Dear My Muse Online Fansign 1.0	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563c2a003b18b07609.png
TXT	The Star Chapter: Sanctuary	Dear My Muse Online Fansign 1.0	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563c3c0033261d441f.png
TXT	The Star Chapter: Sanctuary	Dear My Muse Online Fansign 1.0	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563c57001f16e88762.png
TXT	The Star Chapter: Sanctuary	Dear My Muse Online Fansign 1.0	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563c680003c9bfed61.png
TXT	The Star Chapter: Sanctuary	Barnes & Noble Exclusive	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673956a8000cc4537a3c.png
TXT	The Star Chapter: Sanctuary	Barnes & Noble Exclusive	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67395750000687ca283d.png
TXT	The Star Chapter: Sanctuary	Barnes & Noble Exclusive	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6795bead0011871f6a96.png
TXT	The Star Chapter: Sanctuary	Barnes & Noble Exclusive	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6739578a0024a78427b3.png
TXT	The Star Chapter: Sanctuary	Barnes & Noble Exclusive	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67cf386b001ad99b81d8.png
TXT	The Star Chapter: Sanctuary	Kpop Nara Exclusive	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67698141000685ded57f.png
TXT	The Star Chapter: Sanctuary	Kpop Nara Exclusive	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c0c40031164a226f.png
TXT	The Star Chapter: Sanctuary	Kpop Nara Exclusive	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c0f700182c13a405.png
TXT	The Star Chapter: Sanctuary	Kpop Nara Exclusive	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c10e002b2f92c119.png
TXT	The Star Chapter: Sanctuary	Kpop Nara Exclusive	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67cf384b0022fe2ae7ee.png
TXT	The Star Chapter: Sanctuary	Hello82 Exclusive	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6756017f0037e853c6eb.png
TXT	The Star Chapter: Sanctuary	Hello82 Exclusive	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675601af0033115b8619.png
TXT	The Star Chapter: Sanctuary	Hello82 Exclusive	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675601c9001c2b8140ae.png
TXT	The Star Chapter: Sanctuary	Hello82 Exclusive	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675601e30009a446aa64.png
TXT	The Star Chapter: Sanctuary	Hello82 Exclusive	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6756020300350a1cabd2.png
TXT	The Star Chapter: Sanctuary	Target Exclusive	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67380e5a003cf6bfbbbe.png
TXT	The Star Chapter: Sanctuary	Target Exclusive	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6739542b00310ad9e006.png
TXT	The Star Chapter: Sanctuary	Target Exclusive	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d6ff002c1f691dce.png
TXT	The Star Chapter: Sanctuary	Target Exclusive	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d04c000feea68ad5.png
TXT	The Star Chapter: Sanctuary	Target Exclusive	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6748bcfc0036505e2492.png
TXT	The Star Chapter: Sanctuary	Tower Records Preorder	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563a96002a24b9cf26.png
TXT	The Star Chapter: Sanctuary	Tower Records Preorder	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563af100376a09556e.png
TXT	The Star Chapter: Sanctuary	Tower Records Preorder	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563b2100238e5627f8.png
TXT	The Star Chapter: Sanctuary	Tower Records Preorder	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563b3e002aa2ae582a.png
TXT	The Star Chapter: Sanctuary	Tower Records Preorder	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563b87000c22b74383.png
TXT	The Star Chapter: Sanctuary	HMV Preorder	Soobin A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675a03c9003cd431a249.png
TXT	The Star Chapter: Sanctuary	HMV Preorder	Yeonjun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675a0395000b1440046e.png
TXT	The Star Chapter: Sanctuary	HMV Preorder	Beomgyu A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675a03df00216dcd31b4.png
TXT	The Star Chapter: Sanctuary	HMV Preorder	Taehyun A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675a03f6001104368e71.png
TXT	The Star Chapter: Sanctuary	HMV Preorder	Huening Kai A	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675a040d002ed112dcbc.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675639b700201f341496.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675639d50018d8f6d4ab.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563a040026e84ab27d.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563a3800208f87a7be.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563a6200196dad3a4c.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Preorder Angel Ver.	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675540d7003e4e1e7640.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Preorder Angel Ver.	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755410a0027438eb485.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Preorder Angel Ver.	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755415b00261f57dc3f.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Preorder Angel Ver.	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755418600215959340b.png
TXT	The Star Chapter: Sanctuary	Universal Music Japan Preorder Angel Ver.	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675541b50017c5494b02.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563830002a9d47e943.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563862003a5f6eec78.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675638d7001b282c74f3.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675638ff000022bdad69.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67563935003d3bbe53ef.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Preorder Angel Ver.	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d82300174840d006.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Preorder Angel Ver.	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755dba6003b6a15567a.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Preorder Angel Ver.	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755ff66000d78e310b1.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Preorder Angel Ver.	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755daff002a7fa7f677.png
TXT	The Star Chapter: Sanctuary	Weverse Japan Preorder Angel Ver.	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755db3c002935f55076.png
TXT	The Star Chapter: Sanctuary	CU Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e5460025c24e5045.png
TXT	The Star Chapter: Sanctuary	CU Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e5db000c89221600.png
TXT	The Star Chapter: Sanctuary	CU Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d3f5003e12b14a24.png
TXT	The Star Chapter: Sanctuary	CU Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d41d003ceebba15f.png
TXT	The Star Chapter: Sanctuary	CU Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fc8c000ecf7d42f2.png
TXT	The Star Chapter: Sanctuary	Olive Young Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675541e20025e390689c.png
TXT	The Star Chapter: Sanctuary	Olive Young Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675542080000cf8854a7.png
TXT	The Star Chapter: Sanctuary	Olive Young Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fc1a003700116bb2.png
TXT	The Star Chapter: Sanctuary	Olive Young Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d90a0032b890bdc1.png
TXT	The Star Chapter: Sanctuary	Olive Young Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fc3f0028f7d06e31.png
TXT	The Star Chapter: Sanctuary	Kakaotalk Preorder	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d4960034cf15ffce.png
TXT	The Star Chapter: Sanctuary	Kakaotalk Preorder	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fb4b0008dfd8a1dc.png
TXT	The Star Chapter: Sanctuary	Kakaotalk Preorder	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d4b5002cd1738119.png
TXT	The Star Chapter: Sanctuary	Kakaotalk Preorder	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6756f17b003c07aab3ca.png
TXT	The Star Chapter: Sanctuary	Kakaotalk Preorder	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755dbb60038eb18d352.png
TXT	The Star Chapter: Sanctuary	Kakaotalk Preorder	Group	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67cf38a00001b26b666f.png
TXT	The Star Chapter: Sanctuary	Apple Music Preorder Angel Ver.	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67dd317b002dca356fc6.png
TXT	The Star Chapter: Sanctuary	Apple Music Preorder Angel Ver.	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67dd319d003a4ef87597.png
TXT	The Star Chapter: Sanctuary	Apple Music Preorder Angel Ver.	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67dd31b300343d10528f.png
TXT	The Star Chapter: Sanctuary	Apple Music Preorder Angel Ver.	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67cf37e6001b63c446b8.png
TXT	The Star Chapter: Sanctuary	Makestar Preorder Angel Ver.	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67572def003da685a045.png
TXT	The Star Chapter: Sanctuary	Makestar Preorder Angel Ver.	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67572e0b003160435e78.png
TXT	The Star Chapter: Sanctuary	Makestar Preorder Angel Ver.	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67572e22001deeb9c8e1.png
TXT	The Star Chapter: Sanctuary	Makestar Preorder Angel Ver.	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67572e380032273b649d.png
TXT	The Star Chapter: Sanctuary	Makestar Preorder Angel Ver.	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67572e61002e89bd9374.png
TXT	The Star Chapter: Sanctuary	Ktown4u Preorder Angel Ver. Ticket	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c1af0035a2d00e41.png
TXT	The Star Chapter: Sanctuary	Ktown4u Preorder Angel Ver. Ticket	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c1df00212d2ab2ad.png
TXT	The Star Chapter: Sanctuary	Ktown4u Preorder Angel Ver. Ticket	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c1ef002884d70bfd.png
TXT	The Star Chapter: Sanctuary	Ktown4u Preorder Angel Ver. Ticket	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c201003a1bb1aa42.png
TXT	The Star Chapter: Sanctuary	Ktown4u Preorder Angel Ver. Ticket	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67ce2fd20020fda315c0.png
TXT	The Star Chapter: Sanctuary	Yes24 Preorder Angel Ver.	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d34c001195ffc8cb.png
TXT	The Star Chapter: Sanctuary	Yes24 Preorder Angel Ver.	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67d0c2250026282fcb17.png
TXT	The Star Chapter: Sanctuary	Yes24 Preorder Angel Ver.	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67cd18c3003b542ef4f5.png
TXT	The Star Chapter: Sanctuary	Weverse Global Lucky Draw	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e4df00287d2477bb.png
TXT	The Star Chapter: Sanctuary	Weverse Global Lucky Draw	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e52000119582a1c4.png
TXT	The Star Chapter: Sanctuary	Weverse Global Lucky Draw	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fba0003bedd19077.png
TXT	The Star Chapter: Sanctuary	Weverse Global Lucky Draw	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755d091001f6df3a0ba.png
TXT	The Star Chapter: Sanctuary	Weverse Global Lucky Draw	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fbc70028aa514fa7.png
TXT	The Star Chapter: Sanctuary	Weverse Global Preorder Angel Ver.	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e60e000349e3459a.png
TXT	The Star Chapter: Sanctuary	Weverse Global Preorder Angel Ver.	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e87f000536b699a5.png
TXT	The Star Chapter: Sanctuary	Weverse Global Preorder Angel Ver.	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755cfae002d54efdb6f.png
TXT	The Star Chapter: Sanctuary	Weverse Global Preorder Angel Ver.	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675502dc00200fa22e50.png
TXT	The Star Chapter: Sanctuary	Weverse Global Preorder Angel Ver.	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67553fd6001af2c004ff.png
TXT	The Star Chapter: Sanctuary	Merch Set	Soobin	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e00100240583ce87.png
TXT	The Star Chapter: Sanctuary	Merch Set	Yeonjun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e028002edf2ff2cf.png
TXT	The Star Chapter: Sanctuary	Merch Set	Beomgyu	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e0e5000e3cbb96ca.png
TXT	The Star Chapter: Sanctuary	Merch Set	Taehyun	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e15900132ef7805e.png
TXT	The Star Chapter: Sanctuary	Merch Set	Huening Kai	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754e211000affb62979.png
TXT	The Star Chapter: Sanctuary	Weverse QR Set	Group A	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755ffd6000e2b73521d.png
TXT	The Star Chapter: Sanctuary	Weverse QR Set	Group B	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755fff900054d346533.png
TXT	The Star Chapter: Sanctuary	Weverse QR Set	Group C	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6756000e0013156e102b.png
TXT	The Star Chapter: Sanctuary	Weverse B Set B	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754df570023f9ec5d89.png
TXT	The Star Chapter: Sanctuary	Weverse B Set B	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/674fbe34000dac2098c5.png
TXT	The Star Chapter: Sanctuary	Weverse B Set B	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a6820012ff927b95.png
TXT	The Star Chapter: Sanctuary	Weverse B Set B	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a6ab00093f5313bb.png
TXT	The Star Chapter: Sanctuary	Weverse B Set B	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a6b500253abe3468.png
TXT	The Star Chapter: Sanctuary	Weverse B Set A	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a665001c25748af0.png
TXT	The Star Chapter: Sanctuary	Weverse B Set A	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/674fbe95000881b30845.png
TXT	The Star Chapter: Sanctuary	Weverse B Set A	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67571ba9002b99b6433b.png
TXT	The Star Chapter: Sanctuary	Weverse B Set A	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754d74100215cb59163.png
TXT	The Star Chapter: Sanctuary	Weverse B Set A	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a6d6003e1ffb45e6.png
TXT	The Star Chapter: Sanctuary	Weverse A Set B	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a5e8003adaa1231f.png
TXT	The Star Chapter: Sanctuary	Weverse A Set B	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a5f6002714e2c3cb.png
TXT	The Star Chapter: Sanctuary	Weverse A Set B	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a605002a93ae10e9.png
TXT	The Star Chapter: Sanctuary	Weverse A Set B	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737e05000208668c089.png
TXT	The Star Chapter: Sanctuary	Weverse A Set B	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754dfd400149b8b4892.png
TXT	The Star Chapter: Sanctuary	Weverse A Set A	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a5c00013354cb6f0.png
TXT	The Star Chapter: Sanctuary	Weverse A Set A	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a5cc003d057fb8df.png
TXT	The Star Chapter: Sanctuary	Weverse A Set A	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a5d8003274a42d56.png
TXT	The Star Chapter: Sanctuary	Weverse A Set A	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754dfa2000ed79622aa.png
TXT	The Star Chapter: Sanctuary	Weverse A Set A	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6737df5200040fabc6cd.png
TXT	The Star Chapter: Sanctuary	CD Tray Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c9470015b83ef499.png
TXT	The Star Chapter: Sanctuary	CD Tray Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c9970012712038e0.png
TXT	The Star Chapter: Sanctuary	CD Tray Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c9bd000a2f611d33.png
TXT	The Star Chapter: Sanctuary	CD Tray Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c9e40006fde76bcd.png
TXT	The Star Chapter: Sanctuary	CD Tray Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757ca06003a549801ba.png
TXT	The Star Chapter: Sanctuary	Star Board Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c644001618e783a1.png
TXT	The Star Chapter: Sanctuary	Star Board Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c6be0000d509d7f5.png
TXT	The Star Chapter: Sanctuary	Star Board Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c77900337f1de868.png
TXT	The Star Chapter: Sanctuary	Star Board Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c7ce0010d6f0558b.png
TXT	The Star Chapter: Sanctuary	Star Board Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c83300396ed5e3ed.png
TXT	The Star Chapter: Sanctuary	Postcard Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c4a200207e9f57fe.png
TXT	The Star Chapter: Sanctuary	Postcard Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c5170034e6095119.png
TXT	The Star Chapter: Sanctuary	Postcard Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c53a0002de3e07e4.png
TXT	The Star Chapter: Sanctuary	Postcard Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c55600067a539e39.png
TXT	The Star Chapter: Sanctuary	Postcard Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c574000eed050ae5.png
TXT	The Star Chapter: Sanctuary	Mini Poster Set	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c383001c10249d5f.png
TXT	The Star Chapter: Sanctuary	Mini Poster Set	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c367002d79d45107.png
TXT	The Star Chapter: Sanctuary	Mini Poster Set	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c353002ec791d579.png
TXT	The Star Chapter: Sanctuary	Mini Poster Set	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c2380025f8b7a180.png
TXT	The Star Chapter: Sanctuary	Mini Poster Set	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757c3ca00086a378d74.png
TXT	The Star Chapter: Sanctuary	Angel Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a4c5001bb9d58d79.png
TXT	The Star Chapter: Sanctuary	Angel Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a4d9002f5f34e3ea.png
TXT	The Star Chapter: Sanctuary	Angel Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a4e4001f600f0024.png
TXT	The Star Chapter: Sanctuary	Angel Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a4ef0035b749d9de.png
TXT	The Star Chapter: Sanctuary	Angel Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a4fa003a869db06b.png
TXT	The Star Chapter: Sanctuary	Group Postcard	Group Postcard photocard set	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759fc830038cdfaadfc.png
TXT	The Star Chapter: Sanctuary	Group Postcard	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759fe8d002166401416.png
TXT	The Star Chapter: Sanctuary	Group Poster	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6755423a002aba2fab84.png
TXT	The Star Chapter: Sanctuary	Heart Card Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6738adea003a36084ea6.png
TXT	The Star Chapter: Sanctuary	Heart Card Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754cdf60006458b4842.png
TXT	The Star Chapter: Sanctuary	Heart Card Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/674b5443001dc5e04eef.png
TXT	The Star Chapter: Sanctuary	Heart Card Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754ce1a001d2e6ce025.png
TXT	The Star Chapter: Sanctuary	Heart Card Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754ce3a0000fc12210c.png
TXT	The Star Chapter: Sanctuary	Lover Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a47d001fd6a12362.png
TXT	The Star Chapter: Sanctuary	Lover Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/674fbebf0032ea9b2cba.png
TXT	The Star Chapter: Sanctuary	Lover Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754cda3001a06f4d6a9.png
TXT	The Star Chapter: Sanctuary	Lover Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6738ae21002fa21a7496.png
TXT	The Star Chapter: Sanctuary	Lover Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a4910007202a84e9.png
TXT	The Star Chapter: Sanctuary	Group Postcard	Group Postcard photocard set	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6759fb6e0022a959a4dd.png
TXT	The Star Chapter: Sanctuary	Group Postcard	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757bfb40027d80e23e1.png
TXT	The Star Chapter: Sanctuary	Ice Piece Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/676db85000144c0c5c79.png
TXT	The Star Chapter: Sanctuary	Ice Piece Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6784768f001e208168ff.png
TXT	The Star Chapter: Sanctuary	Ice Piece Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675a1b3600297fbda790.png
TXT	The Star Chapter: Sanctuary	Ice Piece Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67cd18a8002a55225930.png
TXT	The Star Chapter: Sanctuary	Savior Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a450003e4ccd5958.png
TXT	The Star Chapter: Sanctuary	Savior Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754ccca000c2d3652f4.png
TXT	The Star Chapter: Sanctuary	Savior Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/67361b550021119dae0e.png
TXT	The Star Chapter: Sanctuary	Savior Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a45d0006d38444f6.png
TXT	The Star Chapter: Sanctuary	Savior Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754cdd100140147ea30.png
TXT	The Star Chapter: Sanctuary	Group Postcard	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675fab8f002d15ba1b6b.png
TXT	The Star Chapter: Sanctuary	Group Poster	Group	Полая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6757bf1000379d2be7fa.png
TXT	The Star Chapter: Sanctuary	Licence Card Set	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/674bfea200281f9d6b8d.png
TXT	The Star Chapter: Sanctuary	Licence Card Set	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6746077e000ec91b7dca.png
TXT	The Star Chapter: Sanctuary	Licence Card Set	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754cd740015fd87bd9c.png
TXT	The Star Chapter: Sanctuary	Licence Card Set	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/673909210000a6b7e6b5.png
TXT	The Star Chapter: Sanctuary	Licence Card Set	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/675dcc8d0018a2652f22.png
TXT	The Star Chapter: Sanctuary	Knight Set	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a3fd003e2c688426.png
TXT	The Star Chapter: Sanctuary	Knight Set	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a3ea000159d39d8b.png
TXT	The Star Chapter: Sanctuary	Knight Set	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754cd180024e4777d80.png
TXT	The Star Chapter: Sanctuary	Knight Set	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6754cd440027ad2aef50.png
TXT	The Star Chapter: Sanctuary	Knight Set	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6734a40b003bae4a297b.png
TXT	LOVE LANGUAGE	(B)	Yeonjun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/68813560001a71cf24de.png
TXT	LOVE LANGUAGE	(B)	Soobin	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688135710003dd28629f.png
TXT	LOVE LANGUAGE	(B)	Beomgyu	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688135d40037181871f7.png
TXT	LOVE LANGUAGE	(B)	Taehyun	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6881357c001a1d0b641f.png
TXT	LOVE LANGUAGE	(B)	Huening Kai	Редкая	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688135a0003557ad80e9.png
TXT	LOVE LANGUAGE	(A)	Yeonjun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688134b2000d308e9a27.png
TXT	LOVE LANGUAGE	(A)	Soobin	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688133a9000191b794cc.png
TXT	LOVE LANGUAGE	(A)	Beomgyu	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688134ee0008f3d09692.png
TXT	LOVE LANGUAGE	(A)	Taehyun	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688135b6001131f32fdd.png
TXT	LOVE LANGUAGE	(A)	Huening Kai	Обычная	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6881348b0002b37cd66e.png
TXT	The Star Chapter: TOGETHER	Starlight Postcard Set	Soobin	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/68813856001efd4f9334.png
TXT	The Star Chapter: TOGETHER	Starlight Postcard Set	Yeonjun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6881386a0026535e4f20.png
TXT	The Star Chapter: TOGETHER	Starlight Postcard Set	Beomgyu	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688138790014337de61f.png
TXT	The Star Chapter: TOGETHER	Starlight Postcard Set	Taehyun	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/68813890001cb36bf21d.png
TXT	The Star Chapter: TOGETHER	Starlight Postcard Set	Huening Kai	Легендарная 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688138a00026a28b4d20.png
TXT	The Star Chapter: TOGETHER	Awake	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6881362000361399daff.png
TXT	The Star Chapter: TOGETHER	Awake	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/68813641002c6e00b50a.png
TXT	The Star Chapter: TOGETHER	Awake	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/68813668001fa2e70836.png
TXT	The Star Chapter: TOGETHER	Awake	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/6881367e00202b24103a.png
TXT	The Star Chapter: TOGETHER	Awake	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/68813691002c932b13eb.png
TXT	The Star Chapter: TOGETHER	Etched	Soobin	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688137ae003c70026b09.png
TXT	The Star Chapter: TOGETHER	Etched	Yeonjun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688137cc000a58cf8195.png
TXT	The Star Chapter: TOGETHER	Etched	Beomgyu	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688137e80003a79313c0.png
TXT	The Star Chapter: TOGETHER	Etched	Taehyun	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688138000010393f7ea0.png
TXT	The Star Chapter: TOGETHER	Etched	Huening Kai	Эпическая 	https://i.kcollect.net/storage/uploads/app-6376c6832c5255be695a/639079e36d9e6206db27/688138140022e1520e14.png
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