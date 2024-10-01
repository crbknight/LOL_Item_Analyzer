import requests
import os
import time
import re


# Function to get an item's ID by by name
def get_item_id_name(item_name, item_data):
    for item_id, item_info in item_data.items():
        if item_info['name'] == item_name:
            return item_id, item_info
    return None, None

def extract_special_stat(description, stat_name):
    # Pattern to match both percentages and regular numbers for the given stat
    pattern_one = rf"<attention>(\d+%?)</attention> {stat_name}"
    match = re.search(pattern_one, description)
    if match:
        value = match.group(1)
        # If the value is a percentage (ends with '%'), convert it to decimal
        if value.endswith('%'):
            return float(value[:-1]) # Used to convert "18%" to 0.18
        else:
            return int(value)  # Return integer if it's a regular number
        
    # Some descriptions have buffedstats instead of attention
    pattern_two = rf"<buffedStat>(\d+%?)</buffedStat> {stat_name}"
    match = re.search(pattern_two, description)
    if match:
        value = match.group(1)
        # If the value is a percentage (ends with '%'), convert it to decimal
        if value.endswith('%'):
            return float(value[:-1]) # Used to convert "18%" to 0.18
        else:
            return int(value)  # Return integer if it's a regular number
    return 0  # Return 0 if the stat is not found

def calculate_base_gold(current_patch):
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
    basePercentMS = None
    baseFlatMS = None
    baseHealShieldPower = None
    basePercentTenacity = None
    

    # Current best items for base stats
    # TODO maybe make this dynamic? idk if its worth the time
    # https://leagueoflegends.fandom.com/wiki/Gold_efficiency_(League_of_Legends)?so=search
    base_item_names = ["Long Sword", "Glowing Mote", "Amplifying Tome", "Cloth Armor",
                   "Null-Magic Mantle", "Ruby Crystal", "Sapphire Crystal", "Rejuvenation Bead",
                   "Faerie Charm", "Cloak of Agility", "Dagger", "Boots",
                   "Last Whisper", "Forbidden Idol", "Serrated Dirk", "Vampiric Scepter", 
                   "Sorcerer's Shoes", "Blighting Jewel", "Winged Moonplate", "Mercury's Treads"]

    base_values = {}

    for item_name in base_item_names:
        item_id, item_info = get_item_id_name(item_name, item_data)

        # Debug Stuff
        #print(f"Current item: {item_name}")
        #print(f"Current item_id: {item_id}")
        #print(f"Current item_info: {item_info}")

        # TODO need to check that i'm getting the right item, via a map tag? Or some other ID. EX all boots have dupes for arena map (THANKS RIOT)

        if item_id and item_info:
            # GOLD COST DIFFERS FOR SOME ITEMS
            
            gold_cost = item_info.get("gold", {}).get("total", 0)
            stats = item_info.get("stats", {})
            description = item_info.get('description', "")

            # Debug Stuff
            print(f"Current gold cost: {gold_cost}")
            #print(f"Current stats: {stats}")
            #print(f"Current description: {description}")

            # TODO add the calcs with extra stats, should pull temp variables dynamically in case it changes.
            match item_name:
                case "Long Sword":
                    baseAD = extract_special_stat(description, "Attack Damage")
                    print("Found Long Sword!")
                    if baseAD == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseAD = gold_cost / baseAD
                        base_values["AD"] = baseAD
                        print(f"{item_name} (ID: {item_id}), AD Calc: {baseAD}")
            
                case "Dagger":
                    baseAS = extract_special_stat(description, "Attack Speed")
                    print("Found Dagger!")
                    if baseAS == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseAS = gold_cost / baseAS
                        base_values["AS"] = baseAS
                        print(f"{item_name} (ID: {item_id}), AS Calc: {baseAS}")

                case "Cloak of Agility":
                    baseCrit = extract_special_stat(description, "Critical Strike Chance")
                    print(baseCrit)
                    print("Found Cloak of Agility!")
                    if baseCrit == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseCrit = gold_cost / baseCrit
                        base_values["Crit"] = baseCrit
                        print(f"{item_name} (ID: {item_id}), Crit Calc: {baseCrit}")

                case "Serrated Dirk":
                    # Note extra stats: AD
                    baseLethality = extract_special_stat(description, "Lethality")
                    print("Found Serrated Dirk!")
                    if baseLethality == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempAD = extract_special_stat(description, "Attack Damage")
                        tempGold = gold_cost - (tempAD*base_values["AD"])
                        baseLethality = tempGold / baseLethality
                        base_values["Lethality"] = baseLethality
                        print(f"{item_name} (ID: {item_id}), Lethality Calc: {baseLethality}")

                case "Last Whisper":
                    # Note extra stats: AD
                    basePercentArmorPen = extract_special_stat(description,"Armor Penetration")
                    print("Found Last Whisper!")
                    if basePercentArmorPen == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempAD = extract_special_stat(description, "Attack Damage")
                        tempGold = gold_cost - (tempAD*base_values["AD"])
                        basePercentArmorPen = tempGold / basePercentArmorPen
                        base_values["Percent Armor Pen"] = basePercentArmorPen
                        print(f"{item_name} (ID: {item_id}), % Armor Pen Calc: {basePercentArmorPen}")

                case "Amplifying Tome":
                    baseAP = extract_special_stat(description, "Ability Power")
                    print("Found Amplfying Tome!")
                    if baseAP == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseAP = gold_cost / baseAP
                        base_values["AP"] = baseAP
                        print(f"{item_name} (ID: {item_id}), AP Calc: {baseAP}")

                case "Glowing Mote":
                    baseAH = extract_special_stat(description,"Ability Haste")
                    print("Found Glowing Mote!")
                    if baseAH == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseAH = gold_cost / baseAH
                        base_values["AH"] = baseAH
                        print(f"{item_name} (ID: {item_id}), AH Calc: {baseAH}")
                
                # TODO
                case "Blighting Jewel":
                    # Note extra stats: AP
                    basePercentMPen = extract_special_stat(description,"Magic Penetration")
                    print("Found Blighting Jewel!")
                    if basePercentMPen == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempAP = extract_special_stat(description, "Ability Power")
                        tempGold = gold_cost - (tempAP * base_values["AP"])
                        basePercentMPen = tempGold / basePercentMPen
                        base_values["Percent Magic Pen"] = basePercentMPen
                        print(f"{item_name} (ID: {item_id}), % Magic Pen Calc: {basePercentMPen}")

                case "Ruby Crystal":
                    baseHP = extract_special_stat(description, "Health")
                    print("Found Ruby Crystal!")
                    if baseHP == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseHP = gold_cost / baseHP
                        base_values["HP"] = baseHP
                        print(f"{item_name} (ID: {item_id}), HP Calc: {baseHP}")

                case "Cloth Armor":
                    baseArmor = extract_special_stat(description, "Armor")
                    print("Found Cloth Armor!")
                    if baseArmor == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseArmor = gold_cost / baseArmor
                        base_values["Armor"] = baseArmor
                        print(f"{item_name} (ID: {item_id}), Armor Calc: {baseArmor}")

                case "Null-Magic Mantle":
                    baseMR = extract_special_stat(description, "Magic Resist")
                    print("Found Ruby Crystal!")
                    if baseMR == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseMR = gold_cost / baseMR
                        base_values["MR"] = baseMR
                        print(f"{item_name} (ID: {item_id}), MR Calc: {baseMR}")

                case "Rejuvenation Bead":
                    baseHpRegen = extract_special_stat(description,"Base Health Regen")
                    print("Found Rejuvenation Bead!")
                    if baseHpRegen == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseHpRegen = gold_cost / baseHpRegen
                        base_values["HP Regen"] = baseHpRegen
                        print(f"{item_name} (ID: {item_id}), HP Regen Calc: {baseHpRegen}")

                case "Faerie Charm":
                    baseManaRegen = extract_special_stat(description,"Base Mana Regen")
                    print("Found Faerie Charm!")
                    if baseManaRegen == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseManaRegen = gold_cost / baseManaRegen
                        base_values["Mana Regen"] = baseManaRegen
                        print(f"{item_name} (ID: {item_id}), Mana Regen Calc: {baseManaRegen}")

                case "Sapphire Crystal":
                    baseMana = extract_special_stat(description, "Mana")
                    print("Found Sapphire Crystal!")
                    if baseMana == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseMana = gold_cost / baseMana
                        base_values["Mana"] = baseMana
                        print(f"{item_name} (ID: {item_id}), Mana Calc: {baseMana}")

                case "Vampiric Scepter":
                    # Note extra stats: AD
                    baseLifesteal = extract_special_stat(description, "Life Steal")
                    print("Found Vampiric Scepter!")
                    if baseLifesteal == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempAD = extract_special_stat(description, "Attack Damage")
                        tempGold = gold_cost - (tempAD*base_values["AD"])
                        baseLifesteal = tempGold / baseLifesteal
                        base_values["Lifesteal"] = baseLifesteal
                        print(f"{item_name} (ID: {item_id}), Lifesteal Calc: {baseLifesteal}")

                case "Boots":
                    baseFlatMS = extract_special_stat(description, "Move Speed")
                    print("Found Sapphire Crystal!")
                    if baseFlatMS == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        baseFlatMS = gold_cost / baseFlatMS
                        base_values["MS"] = baseFlatMS
                        print(f"{item_name} (ID: {item_id}), Flat MS: {baseFlatMS}")

                case "Forbidden Idol":
                    # Note extra stats: Mana Regen
                    baseHealShieldPower = extract_special_stat(description, "Heal and Shield Power")
                    print("Found Forbidden Idol!")
                    if baseHealShieldPower == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempManaRegen = extract_special_stat(description, "Base Mana Regen")
                        tempGold = gold_cost - (tempManaRegen * base_values["Mana Regen"])
                        baseHealShieldPower = tempGold / baseHealShieldPower
                        base_values["Heal/Shield Power"] = baseHealShieldPower
                        print(f"{item_name} (ID: {item_id}), Heal/Shield Power Calc: {baseHealShieldPower}")

                case "Sorcerer's Shoes":
                    # Note extra stats: MS
                    baseMPen = extract_special_stat(description, "Magic Penetration")
                    print("Found Sorcerer's Shoes!")
                    if baseMPen == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempMS = extract_special_stat(description, "Move Speed")
                        tempGold = gold_cost - (tempMS * base_values["MS"])
                        baseMPen = tempGold / baseMPen
                        base_values["Magic Pen"] = baseMPen
                        print(f"{item_name} (ID: {item_id}), Flat Magic Pen Calc: {baseMPen}")

                case "Winged Moonplate":
                    # Note extra stats: HP
                    basePercentMS = extract_special_stat(description, "Move Speed")
                    print("Found Winged Moonplate!")
                    if basePercentMS == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempHP = extract_special_stat(description, "Health")
                        tempGold = gold_cost - (tempHP * base_values["HP"])
                        basePercentMS = tempGold / basePercentMS
                        base_values["Percent MS"] = basePercentMS
                        # Note wiki is wrong about this, this item gives 4% ms not 5%
                        print(f"{item_name} (ID: {item_id}), % Move Speed Calc: {basePercentMS}")

                case "Mercury's Treads":
                    # Note extra stats: movement speed, MR
                    basePercentTenacity = extract_special_stat(description, "Tenacity")
                    print("Found Mercury's Treads")
                    if basePercentTenacity == 0:
                        print(f"Something went wrong with {item_name}, value is 0")
                    else:
                        tempMS = extract_special_stat(description, "Move Speed")
                        tempMR = extract_special_stat(description, "Magic Resist")
                        print(f"{item_name} debug tempMS: {tempMS}")
                        print(f"{item_name} debug tempMR: {tempMR}")
                        tempGold = gold_cost - ((tempMS * base_values["MS"])+(tempMR * base_values["MR"]))
                        print(f"{item_name} debug gold_cost: {gold_cost}")
                        print(f"{item_name} debug tempGold: {tempGold}")
                        basePercentTenacity = tempGold / basePercentTenacity
                        base_values["Tenacity"] = basePercentTenacity
                        print(f"{item_name} (ID: {item_id}), Tenacity Calc: {basePercentTenacity}")

                case _:
                    print(f"Item '{item_name}' has no matching case.")
        else:
            print(f"Something went wrong with {item_name}, ID: {item_id}")

    return base_values