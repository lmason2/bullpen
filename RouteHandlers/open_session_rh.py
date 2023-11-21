
from RouteHandlers.base_rh import BaseRouteHandler
from fastapi import HTTPException
from Interfaces.postgres_interface import Session
from datetime import datetime

class OpenSessionRouteHandler(BaseRouteHandler):
    def process_route(self):
        try:
            ## Create session object
            ##------------------------------
            try:
                session = Session(datetime.now(), self.decoded_body['session_name'], self.decoded_body['team_id'], True)
            except Exception as error:
                print(error)
                raise HTTPException(500, 'Error creating session', {})


            ## Write to Postgres
            ##------------------------------
            try:
                self.psql_client.add(session)
            except Exception as error:
                print(error)
                raise HTTPException(500, 'Error adding session', {})
            
            self.results = {
                'data': {
                    'session_id': session.session_id
                },
                'message': 'Successfully opened session'
            }
        except Exception as error:
            print(error)
            raise HTTPException(500, 'Error opening session', {})