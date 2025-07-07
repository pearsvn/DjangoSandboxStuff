import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

"""
This file creates a product assigned to the specified user
in the username value below.
"""

endpoint = "http://127.0.0.1:8080/api/products/"
payload = {
    'title': 'New Item',
    'content': 'My Content',
    'price': 11.99,
}

username = os.getenv('API_USERNAME', 'testuser')
token = os.getenv(f'{username.upper()}_TOKEN')
headers = {'Authorization': f'Token {token}'}

post_response = requests.post(endpoint, json=payload, headers=headers)

try:
    response_json = post_response.json()
    print(f"Request Headers: {headers}")
    print("Request Payload: ", json.dumps(response_json, indent=4))
    print(f"Status: {post_response.status_code}")
except ValueError:
    print("Non-JSON response received.")
    print(post_response.text)