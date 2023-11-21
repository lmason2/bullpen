
from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Vendor

class GetVendorsRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            results = self.psql_client.query(Vendor)
            self.results = {
                'data': results,
                'message': 'Successfully retrieved vendors'
            }
            return
        except Exception:
            raise HTTPException(500, 'Error retrieving data', {})