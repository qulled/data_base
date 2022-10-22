# import pandas
# pandas.read_json("products.json").to_excel("output.xlsx")
import json
import tablib


data = tablib.Dataset(headers=['Баркод', 'SKU', 'Артикул','Китегория','Размер','Себестоимость','ИП','Бренд'])
with open('products.json', 'r', encoding="utf-8") as f:
    file = json.load(f)
for i in file:
    data.append([i,file[i][0].get('SKU'),file[i][1].get('article'),file[i][2].get('category'),file[i][3].get('size'),file[i][4].get('cost_price'),file[i][5].get('owner'),file[i][6].get('brand')])
xlsx = data.export('xlsx')
with open('main_db.xlsx', 'wb') as f:
    f.write(xlsx)