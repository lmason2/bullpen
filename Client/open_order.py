'''
/open-order
'''

import requests
import base64
import json
import uuid

BASE_URL = 'http://127.0.0.1:8000/api/backyard/v1/open-order'

HEADERS = {
}

PAYLOAD = {
    'order_id': str(uuid.uuid4()),
    'session_id': '9f768346-8228-44a7-95de-d222a701aca4',
    'product_ids': ['23ca236a-a4c3-45ff-b0ab-6d7a36f4132b', 'c4e658a5-baa5-4df9-b21d-f8fdd2465091'],
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))