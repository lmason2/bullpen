from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import MenuOption

class GetMenuRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            results = self.psql_client.query(MenuOption)
            self.results = {
                'data': results,
                'message': 'Successfully retrieved menu'
            }
            return
        except Exception:
            raise HTTPException(500, 'Error retrieving data', {})