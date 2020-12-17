import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = 'db_albums'
SQL_URL = f'mysql+mysqldb://{os.environ["SQL_USER"]}:{os.environ["SQL_PASSWORD"]}@localhost/'
