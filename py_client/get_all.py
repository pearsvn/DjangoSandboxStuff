import requests
import json

endpoint = "http://127.0.0.1:8080/api/"
get_response = requests.get(endpoint)

try:
    response_json = get_response.json()
    pretty_json = json.dumps(response_json, indent=4)
    print(pretty_json)
except ValueError:
    print("Non-JSON response received.")
    print(get_response)
print(f"Status: {get_response.status_code}")