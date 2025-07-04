import requests
import json

#Make sure to replace the id of the item you intend on changing
id = 5

endpoint = f"http://127.0.0.1:8080/api/{id}/"
update_data = {
    "title": "The Fifth Item",
    "content": "Fifth Item Content",
    "price": "4.99"
}

put_response = requests.put(endpoint, json=update_data)

try:
    response_json = put_response.json()
    print(json.dumps(response_json, indent=4))
except ValueError:
    print("Non-JSON response received.")
    print(put_response.text)
print(f"Status: {put_response.status_code}")