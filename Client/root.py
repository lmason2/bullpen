import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='../bullpen-logs.log', level=int(os.getenv('LOG_LEVEL')))
logger = logging.getLogger(__name__)

logger.debug('Running root.py from Client/')

BASE_URL = os.getenv('BULLPEN_BASE_URL')

response = requests.get('http://127.0.0.1:8000')

print(response.text)
