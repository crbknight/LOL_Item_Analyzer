from functions import calculate_base_gold, get_all_items, calculate_and_export
import requests

version_url = "https://ddragon.leagueoflegends.com/api/versions.json"

current_version_request = requests.get(version_url)
versions = current_version_request.json()

current_patch = versions[0]

# Getting the items
item_url = f"https://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/item.json"
item_response = requests.get(item_url)
items = item_response.json()

item_data = items['data']


print(f"Current Patch Version: {current_patch}")

base_values = calculate_base_gold(current_patch, item_data)

print(base_values)

item_list = get_all_items(item_data)

calculate_and_export(item_data, item_list, base_values, current_patch)