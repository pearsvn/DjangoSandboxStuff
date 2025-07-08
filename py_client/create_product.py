import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

"""
This file creates a product assigned to the specified user
in the username value below.
"""

def create_product():
    endpoint = "http://127.0.0.1:8080/api/products/"
    payload = {
        'title': 'Item',
        'content': 'Content',
        'price': 1.99,
    }

    username = os.getenv('API_USERNAME', 'testuser')
    token = os.getenv(f'{username.upper()}_TOKEN')
    headers = {'Authorization': f'Token {token}'}

    post_response = requests.post(endpoint, json=payload, headers=headers)

    try:
        response_json = post_response.json()
        return {
            'headers': headers,
            'payload': payload,
            'response': response_json,
            'status': post_response.status_code
        }
    except ValueError:
        return {
            # 'headers': headers,
            'payload': payload,
            'response': post_response.text,
            'status': post_response.status_code,
            'non_json': True
        }

if __name__ == "__main__":
    result = create_product()
    # print(f"Request Headers: {result['headers']}")
    print(f"Request Payload: ", json.dumps(result['response'], indent=4))
    print(f"Status: {result['status']}")