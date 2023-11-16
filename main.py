import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='bullpen-logs.log', level=int(os.getenv('LOG_LEVEL')))
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    print(logging.DEBUG)
    logger.debug('Entered / route with function root()')
    return {"message": "Hello World"}
