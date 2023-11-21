import json
import base64

from fastapi import HTTPException

class BaseRouteHandler:
    def __init__(self, request_body, psql_client) -> None:
        self.request_body       = request_body
        self.decoded_body       = json.loads(base64.b64decode(self.request_body).decode())
        self.psql_client        = psql_client
        self.results            = None

        try:
            self.process_route()
        except HTTPException as e:
            raise HTTPException(e.status_code, e.detail, e.headers)

    def process_route(self):
        pass