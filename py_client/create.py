import requests
import json

endpoint = "http://127.0.0.1:8080/api/"
post_response = requests.post(endpoint, json={'title': 'The Fourth Item', 'content': 'Fourth Item Content', 'price': 29.99})

try:
    response_json = post_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(post_response.text)
print(f"Status: {post_response.status_code}")