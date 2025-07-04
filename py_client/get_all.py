import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


endpoint = "http://127.0.0.1:8080/api/products"

# change the second param in below to change user, e.g. <defaultuser>
username = os.getenv('API_USERNAME', 'defaultuser')
token = os.getenv(f'{username.upper()}_TOKEN')
headers = {'Authorization': f'Token {token}'}

get_response = requests.get(endpoint, headers=headers)

try:
    response_json = get_response.json()
    pretty_json = json.dumps(response_json, indent=4)
    print(pretty_json)
except ValueError:
    print("Non-JSON response received.")
    print(get_response)
print(f"Status: {get_response.status_code}")