from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException

from Utils.redis import expand_dictionary_from_hget

class GetSessionOrdersRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            try:
                session_id = self.decoded_body['session_id']
                collapsed_session = self.redis_client.connection.hgetall(session_id)
                session_record = expand_dictionary_from_hget(collapsed_session, dict())
                self.results = {
                    'data': {
                        'orders': session_record,
                    },
                    'message': f'Successfully got orders for session: {session_id}'
                }
            except Exception as error:
                print(error)
                raise HTTPException(500, 'error', {})
        except Exception as error:
            print(error)
            raise Exception(error)