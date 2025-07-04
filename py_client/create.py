import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = "http://127.0.0.1:8080/api/products/"
payload = {
    'title': 'The Nth Item',
    'content': 'Nth Item Content',
    'price': 9.99,
}

token = os.getenv('API_TOKEN')
headers = {'Authorization': f'Token {token}'}

post_response = requests.post(endpoint, json=payload)

try:
    response_json = post_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(post_response.text)
print(f"Status: {post_response.status_code}")