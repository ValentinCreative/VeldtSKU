import pandas as pd
from data import database, get_data, gc


def generate_mk2kits():
    products = []

    data = get_data('MK2')

    # Boucler sur tous les casques
    for index, product in data.iterrows():
        percent_done = round((index + 1) / len(data) * 100)
        print("Progression ", percent_done, "%")
        size = product['Product_Code'].split('-')[-1]

        component = "M1F"
        if size == "XS":
            component = "M2FX"
        if size == "S":
            component = "M2FS"
        if size == "ML":
            component = "M2FM"
        if size == "XL":
            component = "M2FL"

        if product['FamilySKU'] == 'M2FF':

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
                'COMPONENT': component,
            }
            products.append(fullface3)
            fullface4 = {
                'SKU': product['Product_Code'],
                'QTY': 1,
                'COMPONENT': 'M2SS-SM',
            }
            products.append(fullface4)

        if product['FamilySKU'] == 'M2JE':

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
                'SKU': product['Product_Code'],
                'QTY': 1,
                'COMPONENT': component,
            }
            products.append(fullface2)
            fullface3 = {
                'SKU': product['Product_Code'],
                'QTY': 1,
                'COMPONENT': 'M2SS-SM',
            }
            products.append(fullface3)

        if product['FamilySKU'] == 'M2EN':
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
            fullface3 = {
                'SKU':
                product['Product_Code'],
                'QTY':
                1,
                'COMPONENT':
                product['Product_Code'][:2] + 'CH' +
                product['Product_Code'][4:][:5],
            }
            products.append(fullface3)

        if product['FamilySKU'] == 'M2DH':
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

    data_frame = pd.DataFrame(products)
    sheet = gc.open_by_url(database)
    worksheet = sheet.worksheet('MK2KITS')
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
