import pandas as pd
from data import database, get_data, gc
from utils import concat_sku, concat_description


def generate_mk1():

    products = []
    data = get_data()

    # Boucler sur tous les designs
    for design_index, design in data['designs'].iterrows():

        percent_done = round((design_index + 1) / len(data['designs']) * 100)
        print("Progression ", percent_done, "%")
        for size_index, size in data['mark1_sizes'].iterrows():

            for finish_index, finish in data['helmet_finishes'].iterrows():
                finish_eur = 0
                finish_usd = 0
                finish_rmb = 0
                design_eur = 0
                design_usd = 0
                design_rmb = 0

                if design['HelmetFinishes'] == finish['HelmetFinish']:

                    for config_index, config in data['helmet_config'].iterrows(
                    ):

                        if design['Mark1Config'] == config['Mark1Config']:

                            for finish_price_index, finish_price in data[
                                    'finish_and_design_prices'].iterrows():

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
                                                finish['HelmetFinishSKU'],
                                                size['Sizes'],
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
                                            ]),
                                            'SD_EN':
                                            concat_description([
                                                item['Family'],
                                                item[
                                                    'Helmet_Configuration_or_accesori'],
                                                design['DesignDescription'],
                                            ]),
                                            'SD_FR':
                                            concat_description([
                                                item['Family'],
                                                item['SD_FR'],
                                                design['DesignFR'],
                                            ]),
                                            'SD_ES':
                                            concat_description([
                                                item['Family'],
                                                item['SD_ES'],
                                                design['DesignES'],
                                            ]),
                                            'SD_CN':
                                            concat_description([
                                                item['Family'],
                                                item['SD_CN'],
                                                design['DesignCN'],
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
                                            'description_ENlong':
                                            concat_description([
                                                item['Description_EN'],
                                                design['Description_EN'],
                                            ]),
                                            'description_CNlong':
                                            concat_description([
                                                item['Description_CN'],
                                                design['Description_CN'],
                                            ]),
                                            'description_ESlong':
                                            concat_description([
                                                item['Description_ES'],
                                                design['Description_ES'],
                                            ]),
                                            'design':
                                            design['DesignDescription'],
                                            'designFR':
                                            design['DesignFR'],
                                            'designES':
                                            design['DesignES'],
                                            'designCN':
                                            design['DesignCN'],
                                            'FamilySKU':
                                            item['SKU'],
                                            'Finition':
                                            finish['HelmetFinishSKU'],
                                            'Collection':
                                            design['Collection'],
                                            'Size':
                                            size['Sizes'],
                                            'OldSKU':
                                            concat_sku([
                                                design['OldSKU'],
                                                item['OldSKU'],
                                                finish['HelmetFinishSKU'],
                                                size['Sizes'],
                                            ]),
                                        }
                                        products.append(product)

    data_frame = pd.DataFrame(products)
    sheet = gc.open_by_url(database)
    worksheet = sheet.worksheet('MK1')
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
