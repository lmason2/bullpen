'''
/update-order
'''

import requests
import base64
import json
import uuid

BASE_URL = 'http://127.0.0.1:8000/api/backyard/v1/update-order'

HEADERS = {
}

PAYLOAD = {
    "order_id": "53ad392e-a8fd-46a4-9be2-5ace926d87ff",
    "session_id": "9f768346-8228-44a7-95de-d222a701aca4",
    'status': 'delivered',
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))