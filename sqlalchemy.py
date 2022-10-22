from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv('.env ')

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
SSL_KEY = os.getenv('SSL_KEY')


engine = create_engine(f"mysql+mysqlconnector://root:{PASSWORD}@{HOST}:22/mydb")

engine.connect()

print(engine)