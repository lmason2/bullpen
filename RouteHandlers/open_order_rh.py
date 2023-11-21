
from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Transaction
from Utils.redis import collapse_dictionary_for_hset

class OpenOrderRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            ## Get request data
            ##------------------------------
            try:
                order_id        = self.decoded_body['order_id']
                product_ids     = self.decoded_body['product_ids']
                session_id      = self.decoded_body['session_id']
            except Exception as error:
                print(error)
                raise Exception(error)

            ## Create order object
            ##------------------------------
            try:
                transactions = []
                for product_id in product_ids:
                    transaction = Transaction(order_id, product_id, session_id)
                    transactions.append(transaction)
            except Exception as error:
                print(error)
                raise Exception(error)

            ## Push to Redis
            ##------------------------------
            try:
                transactions_hset = []
                for transaction in transactions:
                    transactions_hset.append({
                        'transaction_id': transaction.transaction_id,
                        'product_id': transaction.product_id
                    })
                    order_hset = {
                        order_id: {
                            'order_id': transaction.order_id,
                            'session_id': session_id,
                            'transactions': transactions_hset,
                            'status': 'requested' # requested, received, filled, delivered
                        }
                    }
                    collapsed_dict = collapse_dictionary_for_hset(order_hset, dict(), '')
                    self.redis_client.connection.hset(session_id, mapping=collapsed_dict)

                self.results = {
                    'data': {
                        'order_id': order_id,
                        'session_id': session_id,
                    },
                    'message': 'successfully opened order'
                }
                return
            except Exception as error:
                print(error)
                raise Exception(error)
    
        except Exception:
            raise HTTPException(500, 'Error opening order', {})