import os
from dotenv import load_dotenv

path = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(path, '.env'))
AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
STORAGE_ACCESS_KEY = os.getenv('STORAGE_ACCESS_KEY')
CONN_STRING = os.getenv('CONN_STRING')
RESOURCE_GRP = os.getenv('RESOURCE_GRP')
STORAGE_ACCOUNT = 'ramyaastorage1'

