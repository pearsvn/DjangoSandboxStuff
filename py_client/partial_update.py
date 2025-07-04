import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

"""
This file updates the specified element of a products assigned
to the specified user in the username value below.
"""

#Make sure to replace the id of the item you intend on changing
id = 11
endpoint = f"http://127.0.0.1:8080/api/products/{id}/"

# change the second param in below to change user, e.g. <defaultuser>
username = os.getenv('API_USERNAME', 'testuser')
token = os.getenv(f'{username.upper()}_TOKEN')
headers = {'Authorization': f'Token {token}'}

update_data = {
    "title": "The Item"
}

patch_response = requests.patch(endpoint, json=update_data, headers=headers)

try:
    response_json = patch_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(patch_response.text)
print(f"Status: {patch_response.status_code}")