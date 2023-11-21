from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Stadium

class GetStadiumsRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            self.results = self.psql_client.query(Stadium)
            return
        except Exception:
            raise HTTPException(500, 'Error retrieving data', {})