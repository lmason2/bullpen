'''
/open-session
'''

import requests
import base64
import json

BASE_URL = 'http://127.0.0.1:8000/api/backyard/v1/open-session'

HEADERS = {
}

PAYLOAD = {
    'session_name': 'test_session_one',
    'team_id': '1ff33220-3eb9-448f-bfe7-ed27a76a3f02',
}

encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

response = requests.post(BASE_URL, data=encoded_payload, headers=HEADERS)

json_response = json.loads(response.text)
print(json.dumps(json_response, indent=4))