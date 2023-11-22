'''
/update-order
'''

import requests
import base64
import json
import uuid

BASE_URL = 'http://127.0.0.1:8000/api/bullpen/v1/update-order'

HEADERS = {
}

PAYLOAD = {
    "order_id": "5b678743-8b9f-4830-8046-6b837dfb7b25",
    "session_id": "e020be21-a0e6-4311-acf7-6f6e4453b290",
    'status': 'delivered',
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))