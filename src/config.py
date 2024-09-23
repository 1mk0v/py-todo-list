import os
from dotenv import load_dotenv
load_dotenv()

ROOT_LOGIN = os.getenv('ROOT_LOGIN')
ROOT_PASSWORD = os.getenv('ROOT_PASSWORD')
PATH_TO_DEFAULT_STATUSES = os.getenv('PATH_TO_DEFAULT_STATUSES')