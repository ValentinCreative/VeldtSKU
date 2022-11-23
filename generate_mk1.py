import os
import pandas as pd
import gspread as gs

credentials = {
    "type": os.environ['type'],
    "project_id": os.environ['project_id'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'],
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    "auth_uri": os.environ['auth_uri'],
    "token_uri": os.environ['token_uri'],
    "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url": os.environ['client_x509_cert_url'],
}
database = "https://docs.google.com/spreadsheets/d/1EVUj6VfX5HioFMWWxpn8RseRiHhjBbxuYFtFkXOjPdw/edit#gid=0"
# Liste des fichiers Excel
sources = {
    'designs':
    'https://docs.google.com/spreadsheets/d/1ATdpFQLjA9HMIbfqiO-bTlulv9l4xY_x3w8r87pbpZI/edit#gid=2109979458',
    'finish_and_design_prices':
    'https://docs.google.com/spreadsheets/d/15ffTy1FaD3JVgcw8kQPO2w9vTt_OHkj4mrdfpuLucS4/edit#gid=2040941895',
    'helmet_config':
    'https://docs.google.com/spreadsheets/d/1uFQNNBbIO848TpWdvtFr_R2Kb2qGG5s2iKkHq4WuumY/edit#gid=1156235883',
    'helmet_finishes':
    'https://docs.google.com/spreadsheets/d/1wWip1Bc9XDy9LE-DGkcdsELaCFeB94E0FJE0TiCpDhU/edit#gid=175302935',
    'helmet_items':
    'https://docs.google.com/spreadsheets/d/1aYihc1jH8vR3Kp8Sc9odDsGZA5USjd-kMa2-X2yEfs0/edit#gid=1570741415',
    'mark1_certifications':
    'https://docs.google.com/spreadsheets/d/1HTxz5ypJ-agnC0BzZ1gX6HrW0Xvthn3oFcb1GWV0Oj4/edit#gid=390737500',
    'mark1_sizes':
    'https://docs.google.com/spreadsheets/d/1_B9rce0wINDHBE3QGV0An0NUnJVCBwcz1Ddn6jyk4po/edit#gid=1621514264',
}


def list_mixed_to_str(data):
    return list(map(str, data))


def concat(data, separator):
    return separator.join(list_mixed_to_str(data))


def concat_sku(skus):
    return concat(skus, '-')


def concat_description(descriptions):
    return concat(descriptions, ' ')


def generate_mk1():

    gc = gs.service_account_from_dict(credentials)

    products = []

    # Transforme chaque fichiers en donnée exploitable
    data = {}

    for key in sources:
        print("Récupération du fichier ", key)
        sh = gc.open_by_url(sources[key])
        ws = sh.get_worksheet(0)
        data[key] = pd.DataFrame(ws.get_all_records())

    # Boucler sur tous les designs
    for design_index, design in data['designs'].iterrows():
        percent_done = round((design_index + 1) / len(data['designs']) * 100)
        print("Progression ", percent_done, "%")

        # Boucler sur toutes les tailles
        for size_index, size in data['mark1_sizes'].iterrows():

            # Boucler sur toutes les certifications
            for certification_index, certification in data[
                    'mark1_certifications'].iterrows():

                # Boucler sur toutes les finitions
                for finish_index, finish in data['helmet_finishes'].iterrows():

                    # Si le design correspond à la finition
                    if design['HelmetFinishes'] == finish['HelmetFinish']:

                        # Boucler sur toutes les configurations
                        for config_index, config in data[
                                'helmet_config'].iterrows():

                            # Boucler sur touts les prix / finitions
                            for finish_price_index, finish_price in data[
                                    'finish_and_design_prices'].iterrows():
                                finish_eur = 0
                                finish_usd = 0
                                finish_rmb = 0
                                design_eur = 0
                                design_usd = 0
                                design_rmb = 0

                                if finish_price['Parameter2'] == config[
                                        'Mark1ConfigSKU'] and finish_price[
                                            'Parameter1'] == finish[
                                                'HelmetFinishSKU']:
                                    finish_eur = float(
                                        finish_price['M1PriceEUR'])
                                    finish_usd = float(
                                        finish_price['M1PriceUSD'])
                                    finish_rmb = float(
                                        finish_price['M1PriceRMB'])

                                if finish_price['Parameter1'] == config[
                                        'Mark1ConfigSKU'] and finish_price[
                                            'Parameter2'] == design[
                                                'Mark1PriceCategory']:
                                    design_eur = float(
                                        finish_price['M1PriceEUR'])
                                    design_usd = float(
                                        finish_price['M1PriceUSD'])
                                    design_rmb = float(
                                        finish_price['M1PriceRMB'])

                            # Boucler sur touts les items
                            for item_index, item in data[
                                    'helmet_items'].iterrows():

                                if item['FamilySKU'] == 'M1':
                                    if item['ItemSKU'] == config[
                                            'Mark1ConfigSKU']:
                                        product = {
                                            'Product_Code':
                                            concat_sku([
                                                item['SKU'],
                                                design['DesignSKU'],
                                                finish['HelmetFinish'],
                                                size['Sizes'],
                                                certification[
                                                    'Mark1Certifications'],
                                            ]),
                                            'Description_EN':
                                            concat_description([
                                                item['Family'],
                                                item[
                                                    'Helmet_Configuration_or_accesori'],
                                                design['DesignDescription'],
                                                finish[
                                                    'HelmetFinishDescription'],
                                                size['Sizes'],
                                                certification[
                                                    'Mark1Certifications'],
                                            ]),
                                            'EUR':
                                            item['EUR'] + finish_eur +
                                            design_eur,
                                            'USD':
                                            item['USD'] + finish_usd +
                                            design_usd,
                                            'RMB':
                                            item['RMB'] + finish_rmb +
                                            design_rmb,
                                            'description_FRlong':
                                            concat_description([
                                                item['Description_FR'],
                                                design['Description_FR'],
                                            ]),
                                            'design':
                                            design['DesignDescription'],
                                        }
                                        products.append(product)

    data_frame = pd.DataFrame(products)
    sheet = gc.open_by_url(database)
    worksheet = sheet.get_worksheet(0)
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
