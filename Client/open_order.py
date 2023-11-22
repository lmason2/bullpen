'''
/open-order
'''

import requests
import base64
import json
import uuid

BASE_URL = 'http://127.0.0.1:8000/api/bullpen/v1/open-order'

HEADERS = {
}

PAYLOAD = {
    'order_id': str(uuid.uuid4()),
    "session_id": "3e06ea77-2982-4ba4-ac7a-5553167f3195",
    'product_ids': ["b272afe9-dba8-4d72-a5f2-357bd8502e4e", "c6b428e9-f01b-4697-a09c-a0c5d787bc19"],
    'seat': '13d',
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))