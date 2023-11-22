'''
/open-session
'''

import requests
import base64
import json

BASE_URL = 'http://127.0.0.1:8000/api/bullpen/v1/open-session'

HEADERS = {
}

PAYLOAD = {
    'session_name': 'test_session_one',
    'team_id': "5fa7a7f1-7a35-40a1-b830-038d942a48d0",
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))