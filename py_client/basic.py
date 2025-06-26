import requests

endpoint = "https://httpbin.org/status/200"
endpoint = "https://httpbin.org/anything"

get_request = requests.get(endpoint)
print(get_request.json())
print(get_request.status_code)