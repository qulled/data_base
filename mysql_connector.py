import mysql.connector
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
S_KEY = os.getenv('S_KEY')
S_KEY_2 = os.getenv('S_KEY_2')

connect = mysql.connector.connect(
    host=HOST,
    port=22,
    user=USER,
    passwd=PASSWORD,
    ssl_key	=S_KEY,
    ssl_cert=S_KEY_2
)

cursor = connect.cursor()
cursor.execute("create table product(rollno int primary key, SKU int, article varchar(50), category varchar(50), size varchar(10), cost_price float, owner varchar(30), brand varchar (50)")
connect.close()

