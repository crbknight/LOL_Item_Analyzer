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
    pattern = rf"<attention>(\d+%?)</attention> {stat_name}"
    match = re.search(pattern, description)
    if match:
        value = match.group(1)
        # If the value is a percentage (ends with '%'), convert it to decimal
        if value.endswith('%'):
            return float(value[:-1]) / 100  # Convert "18%" to 0.18
        else:
            return int(value)  # Return integer if it's a regular number
    return 0  # Return 0 if the stat is not found
