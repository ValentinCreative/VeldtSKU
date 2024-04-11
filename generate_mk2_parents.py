import pandas as pd
from data import database, get_data, gc
from utils import concat_sku, concat_description


def generate_mk2_parents():

    products = []
    data = get_data()

    # Boucler sur tous les designs
    for design_index, design in data['designs'].iterrows():
        percent_done = round((design_index + 1) / len(data['designs']) * 100)
        print("Progression ", percent_done, "%")

        # Boucler sur toutes les finitions
        for finish_index, finish in data['helmet_finishes'].iterrows():
            finish_eur = 0
            finish_usd = 0
            finish_rmb = 0
            design_eur = 0
            design_usd = 0
            design_rmb = 0

            # Si le design correspond à la finition
            if design['HelmetFinishes'] == finish['HelmetFinish']:

                # Boucler sur toutes les configurations
                for config_index, config in data['helmet_config'].iterrows():

                    # Si le design correspond à la config
                    if design['Mark2Config'] == config['Mark2Config']:
                        # Boucler sur touts les prix / finitions
                        for finish_price_index, finish_price in data[
                                'finish_and_design_prices'].iterrows():

                            if finish_price['Parameter2'] == config[
                                    'Mark2ConfigSKU'] and finish_price[
                                        'Parameter1'] == finish[
                                            'HelmetFinishSKU']:
                                finish_eur = float(finish_price['M2PriceEUR'])
                                finish_usd = float(finish_price['M2PriceUSD'])
                                finish_rmb = float(finish_price['M2PriceRMB'])

                            if finish_price['Parameter1'] == config[
                                    'Mark2ConfigSKU'] and finish_price[
                                        'Parameter2'] == design[
                                            'Mark2PriceCategory']:
                                design_eur = float(finish_price['M2PriceEUR'])
                                design_usd = float(finish_price['M2PriceUSD'])
                                design_rmb = float(finish_price['M2PriceRMB'])

                        # Boucler sur tous les items
                        for item_index, item in data['helmet_items'].iterrows(
                        ):

                            if item['FamilySKU'] == 'M2':
                                if item['ItemSKU'] == config['Mark2ConfigSKU']:
                                    product = {
                                        'Product_Code':
                                        concat_sku([
                                            item['SKU'],
                                            design['DesignSKU'],
                                        ]),
                                        'Description_EN':
                                        concat_description([
                                            item['Family'],
                                            item[
                                                'Helmet_Configuration_or_accesori'],
                                            design['DesignDescription'],
                                        ]),
                                        'EUR':
                                        item['EUR'] + finish_eur + design_eur,
                                        'USD':
                                        item['USD'] + finish_usd + design_usd,
                                        'RMB':
                                        item['RMB'] + finish_rmb + design_rmb,
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
                                        'FamilySKU':
                                        item['SKU'],
                                        'Collection':
                                        design['Collection'],
                                    }
                                    products.append(product)

    data_frame = pd.DataFrame(products)
    sheet = gc.open_by_url(database)
    worksheet = sheet.worksheet('MK2P')
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
