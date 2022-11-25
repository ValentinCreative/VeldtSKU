import pandas as pd
import gspread as gs
from credentials import credentials
from data import database


def generate_mk1kits():

    gc = gs.service_account_from_dict(credentials)

    products = []

    sh = gc.open_by_url(database)
    ws = sh.worksheet('MK1')
    data = pd.DataFrame(ws.get_all_records())

    # Boucler sur tous les casques
    for index, product in data.iterrows():
        percent_done = round((index + 1) / len(data) * 100)
        print("Progression ", percent_done, "%")

        if product['FamilySKU'] == 'M1FF':
            fullface = {
                'SKU':
                product['Product_Code'],
                'QTY':
                1,
                'COMPONENT':
                product['Product_Code'][:2] + 'SI' +
                product['Product_Code'][4:],
            }
            products.append(fullface)
            fullface2 = {
                'SKU':
                product['Product_Code'],
                'QTY':
                1,
                'COMPONENT':
                product['Product_Code'][:2] + 'CH' +
                product['Product_Code'][4:][:5],
            }
            products.append(fullface2)
            fullface3 = {
                'SKU': product['Product_Code'],
                'QTY': 1,
                'COMPONENT': 'M1FS',
            }
            products.append(fullface3)
            fullface4 = {
                'SKU': product['Product_Code'],
                'QTY': 1,
                'COMPONENT': 'M1SS-CL',
            }
            products.append(fullface4)

        if product['FamilySKU'] == 'M1EN':
            fullface = {
                'SKU':
                product['Product_Code'],
                'QTY':
                1,
                'COMPONENT':
                product['Product_Code'][:2] + 'SI' +
                product['Product_Code'][4:],
            }
            products.append(fullface)
            fullface2 = {
                'SKU':
                product['Product_Code'],
                'QTY':
                1,
                'COMPONENT':
                product['Product_Code'][:2] + 'CH' +
                product['Product_Code'][4:][:5],
            }
            products.append(fullface2)
            fullface3 = {
                'SKU': product['Product_Code'],
                'QTY': 1,
                'COMPONENT': 'M1PK-BM',
            }
            products.append(fullface3)

    data_frame = pd.DataFrame(products)
    sheet = gc.open_by_url(database)
    worksheet = sheet.worksheet('MK1KITS')
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
