
from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Team

class GetTeamsRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            results = self.psql_client.query(Team)
            self.results = {
                'data': results,
                'message': 'Successfully retrieved teams'
            }
            return
        except Exception:
            raise HTTPException(500, 'Error retrieving data', {})