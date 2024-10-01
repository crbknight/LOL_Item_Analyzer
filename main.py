from functions import *
import requests

version_url = "https://ddragon.leagueoflegends.com/api/versions.json"

current_version_request = requests.get(version_url)
versions = current_version_request.json()

current_patch = versions[0]

print(f"Current Patch Version: {current_patch}")

calculate_base_gold(current_patch)
    