import requests
import json

endpoint = "http://127.0.0.1:8080/api/"

get_response = requests.get(endpoint, params={'title': 'The Fourth Item'})

try:
    response_json = get_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(get_response.text)
print(f"Status: {get_response.status_code}")