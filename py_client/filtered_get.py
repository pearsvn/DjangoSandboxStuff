import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

"""
This file returns the filtered products assigned to the specified user
in the username value below.
"""

endpoint = "http://127.0.0.1:8080/api/products"

# change the second param in below to change user, e.g. <defaultuser>
username = os.getenv('API_USERNAME', 'testuser')
token = os.getenv(f'{username.upper()}_TOKEN')
headers = {'Authorization': f'Token {token}'}

get_response = requests.get(endpoint, params={'id': 11}, headers=headers)

try:
    response_json = get_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(get_response.text)
print(f"Status: {get_response.status_code}")