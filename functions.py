import requests
import os
import time

# Function to get an item's ID by by name
def get_item_id_name(item_name, item_data):
    for item_id, item_info in item_data.items():
        if item_info['name'] == item_name:
            return item_id, item_info
    return None, None