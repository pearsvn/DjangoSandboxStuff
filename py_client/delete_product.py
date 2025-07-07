import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

"""
This file returns all the products assigned to the specified user
in the username value below.
"""
id = 17
endpoint = f"http://127.0.0.1:8080/api/products/{id}/"

# change the second param in below to change user, e.g. <defaultuser>
username = os.getenv('API_USERNAME', 'testuser')
token = os.getenv(f'{username.upper()}_TOKEN')
headers = {'Authorization': f'Token {token}'}

delete_response = requests.delete(endpoint, headers=headers)

if delete_response.status_code==204:
    print(f"✅ Successfully deleted products with ID {id}.")
elif delete_response.status_code==204:
    try:
        response_json = delete_response.json()
        pretty_json = json.dumps(response_json, indent=4)
        print(f"✅ Product deleted successfully. Response: \n{pretty_json}")
    except ValueError:
        print("✅ Product deleted successfully. Non-JSON response received.")
        print(delete_response.text)
elif delete_response.status_code==404:
    print(f"❌ Product with ID {id} not found.")
    print(f"Status: {delete_response.status_code}")
else:
    print(f"⚠️ Unexpected status code: {delete_response.status_code}")
    try:
        response_json = delete_response.json()
        pretty_json = json.dumps(response_json, indent=4)
        print(f"Response: \n{pretty_json}")
    except ValueError:
        print("Non-JSON response received.")
        print(delete_response.text)