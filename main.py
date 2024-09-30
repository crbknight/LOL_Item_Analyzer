from functions import *
import requests

version_url = "https://ddragon.leagueoflegends.com/api/versions.json"

current_version_request = requests.get(version_url)
versions = current_version_request.json()

current_patch = versions[0]

print(f"Current Patch Version: {current_patch}")

# Getting the items
item_url = f"https://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/item.json"
item_response = requests.get(item_url)
items = item_response.json()

item_data = items['data']

# Base stats used for gold efficiencies
# TODO refactor names with "_" instead of camel case (idk why i did this)
baseAD = None
baseAS = None
baseCrit = None
baseLethality = None
basePercentArmorPen = None
baseAP = None
baseAH = None
baseMPen = None
basePercentMPen = None
baseHP = None
baseArmor = None
baseMR = None
baseHpRegen = None
baseManaRegen = None
baseMana = None
baseLifesteal = None
baseOmnivamp = None
basePercentMS = None
baseFlatMS = None
baseHealShieldPower = None
basePercentTenacity = None
basePercentSlowResist = None
basePercentSlow = None

# Current best items for base stats
# TODO maybe make this dynamic? idk if its worth the time
base_item_names = ["Long Sword","Dagger","Cloak of Agility", "Serrated Dirk", "Last Whisper", "Amplifying tome",
                   "Glowing Mote", "MPEN (TODO)", "Blighting Jewel", "Ruby Crystal", "Cloth Armor", "Null-Magic Mantle"
                   "Rejuvination Bead", "Faerie Charm", "Sapphire Crystal", "Vampiric Scepter", "Leeching Leer",
                   "Winged Moonplate", "Boots", "Forbidden Idol", "Mercury Treads", "Boots of Swiftness", "Boots of Swiftness"]

base_stats = {}

for item_name in base_item_names:
    item_id, item_info = get_item_id_name(item_name, item_data)

    if item_id and item_info:
        gold_cost = item_info.get("gold", {}).get("total", 0)
        stats = item_info.get("stats", {})

        match item_name:
            case "Long Sword":
                baseAD = stats.get("FlatPhysicalDamageMod")
                print("Found Long Sword!")
                print(f"{item_name} (ID: {item_id}), AD: {baseAD}")
            
            case "Dagger":
                baseAS = stats.get("PercentAttackSpeedMod")
                print("Found Dagger!")
                print(f"{item_name} (ID: {item_id}), AS: {baseAS}")

            case "Cloak of Agility":
                baseCrit = stats.get("FlatCritChanceMod")
                print("Found Cloak of Agility!")
                print(f"{item_name} (ID: {item_id}), Crit: {baseCrit}")

            case "Serrated Dirk":
                # Note extra stats
                # TODO fix?
                baseLethality = stats.get("Lethality")
                print("Found Serrated Dirk!")
                print(f"{item_name} (ID: {item_id}), Lethality: {baseLethality}")

            case "Last Whisper":
                # Note extra stats
                basePercentArmorPen = stats.get("PercentArmorPenetrationMod")
                print("Found Last Whisper!")
                print(f"{item_name} (ID: {item_id}), % Armor Pen: {basePercentArmorPen}")

            case _:
                print(f"Item '{item_name}' has no matching case.")