from pb_client import PBClient
from config import ACHIEVEMENT_REWARDS

pb = PBClient()

def main():
    users = pb.get_all_users()
    for user in users:
        user_id = user["id"]
        user_cards = pb.get_user_inventory(user_id)
        # Собираем все (group, album) где есть карточки
        collections = set()
        for c in user_cards:
            card = c.get("expand", {}).get("card_id", {})
            group = card.get("group", "-")
            album = card.get("album", "-")
            if group and album:
                collections.add((group, album))
        for group, album in collections:
            all_cards = pb.get_cards_by_group_album(group, album)
            user_card_map = {c.get("expand", {}).get("card_id", {}).get("id"): c.get("count", 0)
                             for c in user_cards
                             if c.get("expand", {}).get("card_id", {}).get("group", "-") == group and
                                c.get("expand", {}).get("card_id", {}).get("album", "-") == album}
            have = sum(1 for card in all_cards if user_card_map.get(card.get("id"), 0) > 0)
            percent = int(have / max(1, len(all_cards)) * 100)
            ach_level = 0
            if percent >= 100:
                ach_level = 4
            elif percent >= 75:
                ach_level = 3
            elif percent >= 50:
                ach_level = 2
            elif percent >= 25:
                ach_level = 1
            if ach_level > 0:
                ach = pb.get_collection_achievement(user_id, group, album)
                prev_level = ach["level"] if ach else 0
                if ach_level > prev_level:
                    reward = ACHIEVEMENT_REWARDS.get(ach_level, {"exp": 0, "stars": 0})
                    pb.set_collection_achievement(user_id, group, album, ach_level)
                    # Обновляем опыт и звёзды
                    new_exp = user.get("exp", 0) + reward["exp"]
                    new_stars = user.get("stars", 0) + reward["stars"]
                    pb.update_user_stars_and_pity(user_id, new_stars, user.get("pity_legendary", 0), user.get("pity_void", 0))
                    pb.add_exp_and_check_levelup(user_id, user.get("level", 1), user.get("exp", 0), reward["exp"])
                    print(f"User {user.get('name')} ({user_id}) получил ачивку {ach_level*25}% за {group} — {album}")

if __name__ == '__main__':
    main() 