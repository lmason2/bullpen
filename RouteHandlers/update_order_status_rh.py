
from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Utils.redis import expand_dictionary_from_hget, collapse_dictionary_for_hset
import json

class UpdateOrderStatusRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            ## Get order object
            ##------------------------------
            try:
                order_id = self.decoded_body['order_id']
                session_id = self.decoded_body['session_id']
                collapsed_session = self.redis_client.connection.hgetall(session_id)
                session_record = expand_dictionary_from_hget(collapsed_session, dict())
                order_record = session_record[order_id]
            except Exception as error:
                print(error)
                raise Exception(error)

            ## Update order status
            ##------------------------------
            try:
                order_status = self.decoded_body['status']
                order_record['status'] = order_status
                collapsed_dictionary = collapse_dictionary_for_hset({order_id: order_record}, dict(), '')
                self.redis_client.connection.hset(session_id, mapping=collapsed_dictionary)

                self.results = {
                    'data': {
                        'order_id': order_id,
                    },
                    'message': f'Successfully updated status to: {order_status}'
                }
                return
            except Exception as error:
                print(error)
                raise Exception(error)

            ## Update Redis
            ##------------------------------
            return
        except Exception:
            raise HTTPException(500, 'Error updating order', {})