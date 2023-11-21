'''
/close-session
'''

import requests
import base64
import json

BASE_URL = 'http://127.0.0.1:8000/api/backyard/v1/close-session'

HEADERS = {
}

PAYLOAD = {
    'session_id': '6093928c-0b5b-4ebc-8746-953e41249b25'
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))