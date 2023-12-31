import logging
from fastapi import HTTPException
from RouteHandlers.get_menu_rh import GetMenuRouteHandler
from RouteHandlers.get_products_rh import GetProductsRouteHandler
from RouteHandlers.get_stadiums_rh import GetStadiumsRouteHandler
from RouteHandlers.get_teams_rh import GetTeamsRouteHandler
from RouteHandlers.get_vendors_rh import GetVendorsRouteHandler
from RouteHandlers.open_session_rh import OpenSessionRouteHandler
from RouteHandlers.close_session_rh import CloseSessionRouteHandler
from RouteHandlers.open_order_rh import OpenOrderRouteHandler
from RouteHandlers.update_order_status_rh import UpdateOrderStatusRouteHandler

ROUTE_MAP = {
    'get-stadiums': GetStadiumsRouteHandler,
    'get-products': GetProductsRouteHandler,
    'get-vendors': GetVendorsRouteHandler,
    'get-teams': GetTeamsRouteHandler,
    'get-menu': GetMenuRouteHandler,
    'open-session': OpenSessionRouteHandler,
    'close-session': CloseSessionRouteHandler,
    'open-order': OpenOrderRouteHandler,
    'update-order': UpdateOrderStatusRouteHandler,
}

class RouteHandlerFactory:
    @staticmethod
    def get_handler(route_endpoint, request_body, psql_client, redis_client):
        route_handler = None
        try:
            if route_endpoint in ROUTE_MAP:
                route_handler = ROUTE_MAP.get(route_endpoint)(request_body, psql_client, redis_client)
                return route_handler
            else:
                logging.error(f'Invalid route: {route_endpoint}')
                raise HTTPException(404, f'Invalid route: {route_endpoint}')
        except HTTPException as e:
            raise HTTPException(e.status_code, e.detail, e.headers)
        except Exception as e:
            raise HTTPException(500, 'Internal Error', {})
    