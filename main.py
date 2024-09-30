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
# Maybe move this into its own function?
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
# TODO Reorder so that base stats come fires so calculations be done for secondaries via:
# https://leagueoflegends.fandom.com/wiki/Gold_efficiency_(League_of_Legends)?so=search
base_item_names = ["Long Sword","Dagger","Cloak of Agility", "Serrated Dirk", "Last Whisper", "Amplifying Tome",
                   "Glowing Mote", "MPEN (TODO)", "Blighting Jewel", "Ruby Crystal", "Cloth Armor", "Null-Magic Mantle",
                   "Rejuvenation Bead", "Faerie Charm", "Sapphire Crystal", "Vampiric Scepter",
                   "Winged Moonplate", "Boots", "Forbidden Idol", "Mercury Treads", "Boots of Swiftness", "Boots of Swiftness"]

base_stats = {}

# Probably move this into its own seperate function
# Also might want to consider moving to the regex function for ALL stats
for item_name in base_item_names:
    item_id, item_info = get_item_id_name(item_name, item_data)

    # Debug Stuff
    #print(f"Current item: {item_name}")
    #print(f"Current item_id: {item_id}")
    #print(f"Current item_info: {item_info}")

    if item_id and item_info:
        gold_cost = item_info.get("gold", {}).get("total", 0)
        stats = item_info.get("stats", {})
        description = item_info.get('description', "")

        # Debug Stuff
        #print(f"Current gold cost: {gold_cost}")
        #print(f"Current stats: {stats}")
        print(f"Current description: {description}")


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
                baseLethality = extract_special_stat(description, "Lethality")
                print("Found Serrated Dirk!")
                print(f"{item_name} (ID: {item_id}), Lethality: {baseLethality}")

            case "Last Whisper":
                # Note extra stats
                basePercentArmorPen = extract_special_stat(description,"Armor Penetration")
                print("Found Last Whisper!")
                print(f"{item_name} (ID: {item_id}), % Armor Pen: {basePercentArmorPen}")

            case "Amplifying Tome":
                baseAP = stats.get("FlatMagicDamageMod")
                print("Found Amplfying Tome!")
                print(f"{item_name} (ID: {item_id}), AP: {baseAP}")

            case "Glowing Mote":
                baseAH = extract_special_stat(description,"Ability Haste")
                print("Found Glowing Mote!")
                print(f"{item_name} (ID: {item_id}), AH: {baseAH}")

            case "Blighting Jewel":
                basePercentMPen = extract_special_stat(description,"Magic Penetration")
                print("Found Blighting Jewel!")
                print(f"{item_name} (ID: {item_id}), % Magic Pen: {basePercentMPen}")

            case "Ruby Crystal":
                baseHP = stats.get("FlatHPPoolMod")
                print("Found Ruby Crystal!")
                print(f"{item_name} (ID: {item_id}), HP: {baseHP}")

            case "Cloth Armor":
                baseArmor = stats.get("FlatArmorMod")
                print("Found Cloth Armor!")
                print(f"{item_name} (ID: {item_id}), Armor: {baseArmor}")

            case "Null-Magic Mantle":
                baseMR = stats.get("FlatSpellBlockMod")
                print("Found Ruby Crystal!")
                print(f"{item_name} (ID: {item_id}), MR: {baseMR}")

            case "Rejuvenation Bead":
                baseHpRegen = extract_special_stat(description,"Base Health Regen")
                print("Found Rejuvenation Bead!")
                print(f"{item_name} (ID: {item_id}), HP Regen: {baseHpRegen}")

            case "Faerie Charm":
                baseManaRegen = extract_special_stat(description,"Base Mana Regen")
                print("Found Faerie Charm!")
                print(f"{item_name} (ID: {item_id}), HP Regen: {baseManaRegen}")

            case "Sapphire Crystal":
                baseMana = stats.get("FlatMPPoolMod")
                print("Found Sapphire Crystal!")
                print(f"{item_name} (ID: {item_id}), Mana: {baseMana}")

            case "Vampiric Scepter":
                baseLifesteal = stats.get("PercentLifeStealMod")
                print("Found Sapphire Crystal!")
                print(f"{item_name} (ID: {item_id}), Lifesteal: {baseLifesteal}")

            case "Vampiric Scepter":
                baseLifesteal = stats.get("PercentLifeStealMod")
                print("Found Sapphire Crystal!")
                print(f"{item_name} (ID: {item_id}), Lifesteal: {baseLifesteal}")

            case _:
                print(f"Item '{item_name}' has no matching case.")
    else:
        print(f"Something went wrong with {item_name}, ID: {item_id}")
    