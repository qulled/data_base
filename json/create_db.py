import json
import time
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import os
import datetime as dt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, 'logs/')
log_file = os.path.join(BASE_DIR, 'logs/parser.log')
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=100000,
    backupCount=3,
    encoding='utf-8'
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s',
    handlers=(
        file_handler,
        console_handler
    )
)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials_service.json'
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
service = discovery.build('sheets', 'v4', credentials=credentials)
START_POSITION_FOR_PLACE = 0

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv('.env ')

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SPREADSHEET_ID_ORDER = os.getenv('SPREADSHEET_ID_ORDER')


def main_db(range_name, table_id):
    dict_products = {}
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=table_id,
                                range=range_name, majorDimension='ROWS').execute()
    results = result.get('values', [])
    for rows in results[1:]:
        try:
            dict_products[rows[5]] = {'SKU': rows[3]}, {'article': rows[4]}, {'category': rows[2]}, {'size': rows[6]}, {
                'cost_price': rows[7]}, {'owner': rows[0]}, {'brand': rows[1]}
        except:
            pass
    with open(f'products.json', 'w', encoding='UTF-8') as json_file:
        json.dump(dict_products, json_file, ensure_ascii=False, indent=2)


def order_db(range_name, table_id):
    dict_products = {}
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=table_id,
                                range=range_name, majorDimension='ROWS').execute()
    results = result.get('values', [])
    count = 4
    for rows in results[2:]:
        try:
            dict_products[rows[6]] = {'full_price': int(rows[9].replace(' ','').replace('₽',''))}, {'category': rows[2]}, {'raiting': rows[11]}, \
                                     {'reviews': rows[12]}, {'search': rows[4]}, {'owner': rows[0]}, \
                                     {'brand': rows[1]}, {'name': rows[3]},{'FBS': []},{'FBO': []},\
                                     {'count': []},{'place': []}
            for i in range(len(rows)+1):
                if i>13 and count%6 == 0:
                    if rows[i] == '':
                        dict_products[rows[6]][8]['FBS'].append({results[1][i][:10]: 0})
                    else:
                        dict_products[rows[6]][8]['FBS'].append({results[1][i][:10]: int(rows[i])})
                    if rows[i+1] == '':
                        dict_products[rows[6]][9]['FBO'].append({results[1][i][:10]: 0})
                    else:
                        dict_products[rows[6]][9]['FBO'].append({results[1][i][:10]: int(rows[i+1])})
                    if rows[i+2] == '':
                        dict_products[rows[6]][10]['count'].append({results[1][i][:10]: 0})
                    elif ' ' in rows[i+2]:
                        price = int(rows[i+2].replace(' ','').replace('₽',''))
                        dict_products[rows[6]][10]['count'].append({results[1][i][:10]: price})
                    if rows[i+3] == '':
                        dict_products[rows[6]][11]['place'].append({results[1][i][:10]: 0})
                    else:
                        dict_products[rows[6]][11]['place'].append({results[1][i][:10]: rows[i+3].strip()})
                count +=1
        except Exception as e:
            # print(e)
            pass
    with open(f'products_order.json', 'w', encoding='UTF-8') as json_file:
        json.dump(dict_products, json_file, ensure_ascii=False, indent=2)


def main_db(range_name, table_id):
    dict_products = {}
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=table_id,
                                range=range_name, majorDimension='ROWS').execute()
    results = result.get('values', [])
    for rows in results[1:]:
        try:
            dict_products[rows[5]] = {'SKU': rows[3]}, {'article': rows[4]}, {'category': rows[2]}, {'size': rows[6]}, {
                'cost_price': rows[7]}, {'owner': rows[0]}, {'brand': rows[1]}
        except:
            pass
    with open(f'products.json', 'w', encoding='UTF-8') as json_file:
        json.dump(dict_products, json_file, ensure_ascii=False, indent=2)


def reader_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        file = json.load(f)
    for i in file:
        print(file[i])


if __name__ == '__main__':
    date = dt.datetime.now()
    day, month, year = date.strftime('%d'), date.strftime('%m'), date.strftime('%Y')
    table_id = SPREADSHEET_ID
    table_id_order = SPREADSHEET_ID_ORDER
    # main_db('Товары', table_id)
    order_db(f'09.{year}', table_id_order)
    # json_file = 'products.json'
    # reader_json(json_file)
