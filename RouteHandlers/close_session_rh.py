
from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Session, Transaction
from Utils.redis import expand_dictionary_from_hget

class CloseSessionRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            
            ## Get all transaction objects
            ##------------------------------
            try:
                session_id = self.decoded_body['session_id']
                collapsed_session = self.redis_client.connection.hgetall(session_id)
                session_record = expand_dictionary_from_hget(collapsed_session, dict())
            except Exception as error:
                print(error)
                raise Exception(error)
            

            ## Close outstanding transactions
            ##------------------------------
            transactions = []
            try:
                for _, v in session_record.items():
                    if v['status'] != 'delivered':
                        v['status'] = 'unfulfilled'
                    transactions = ['transactions']
                    for transaction in transactions:
                        p_transaction = Transaction(v['order_id'], transaction['product_id'], session_id) # add status
                        transactions.append(p_transaction)
            except Exception as error:
                print(error)
                raise Exception(error)
            
            ## Write transactions to postgres
            ##------------------------------

            ## Delete transactions from redis
            ##------------------------------
            try:
                self.redis_client.connection.delete(session_id)
                pass
            except Exception as error:
                print(error)
                raise Exception(error)

            ## Close session
            ##------------------------------
            try:
                results = self.psql_client.session.query(Session).filter(Session.session_id == session_id)
                for session in results:
                    session.active = False
                    self.psql_client.session.commit()
                    self.results = {
                        'data': {
                            'session_id': session_id
                        },
                        'message': 'Successfully closed session'
                    }
                    return
                
                self.results = {
                    'data': [],
                    'message': 'No session found'
                }
            except Exception as error:
                print(error)
                raise Exception(error)
        except Exception:
            raise HTTPException(500, 'Error closing session', {})