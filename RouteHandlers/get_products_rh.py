from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Product

class GetProductsRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            self.results = self.psql_client.query(Product)
            return
        except Exception:
            raise HTTPException(500, 'Error retrieving data', {})