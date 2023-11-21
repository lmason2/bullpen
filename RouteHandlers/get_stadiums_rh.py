from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Stadium

class GetStadiumsRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            results = self.psql_client.query(Stadium)
            self.results = {
                'data': results,
                'message': 'Successfully retrieved stadiums'
            }
            return
        except Exception as error:
            print(error)
            raise HTTPException(500, 'Error retrieving data', {})