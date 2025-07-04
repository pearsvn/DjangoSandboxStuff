import requests
import json

#Make sure to replace the id of the item you intend on changing
id = 2

endpoint = f"http://127.0.0.1:8080/api/{id}/"
update_data = {
    "title": "The Second Item"
}

patch_response = requests.patch(endpoint, json=update_data)

try:
    response_json = patch_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(patch_response.text)
print(f"Status: {patch_response.status_code}")