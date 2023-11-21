import os
import logging
from typing_extensions import Annotated
from fastapi import Depends, FastAPI, Request
from dotenv import load_dotenv
from pydantic import Base64Bytes, BaseModel

from Factories.route_handler_factory import RouteHandlerFactory
from Interfaces.postgres_interface import PostgresClient

load_dotenv()

logging.basicConfig(filename='bullpen-logs.log', level=int(os.getenv('LOG_LEVEL')))
logger = logging.getLogger(__name__)

app = FastAPI()

class RequestModel(BaseModel):
    base64_bytes: Base64Bytes

async def parse_body(request: Request):
    data: bytes = await request.body()
    return data

ParsingDependency = Annotated[str, Depends(parse_body)]

@app.get("/health-check")
async def root():
    return {"status": "Alive"}

@app.post('/api/backyard/v1/{route_endpoint}')
async def handle_route(request: Request, route_endpoint, request_body: ParsingDependency):
    route_handler = RouteHandlerFactory.get_handler(route_endpoint, request_body, psql_client=request.app.state.psql_client)
    return route_handler.results

@app.on_event('startup')
async def startup():
    app.state.psql_client   = PostgresClient('lukemason', 'Lukrative11!', 'localhost', '5432', 'bullpen')
