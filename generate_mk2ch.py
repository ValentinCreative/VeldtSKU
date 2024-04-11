import pandas as pd
from data import database, get_data, gc
from utils import concat_sku, concat_description


def generate_mk2ch():

    products = []
    data = get_data()

    # Boucler sur tous les designs
    for design_index, design in data['designs'].iterrows():
        percent_done = round((design_index + 1) / len(data['designs']) * 100)
        print("Progression ", percent_done, "%")
        # Boucler sur toutes les finitions
        for finish_index, finish in data['helmet_finishes'].iterrows():
            price_eur = 0
            price_usd = 0
            price_rmb = 0
            # Si le design correspond à la finition
            if design['HelmetFinishes'] == finish['HelmetFinish']:

                # Boucler sur touts les prix / finitions
                for finish_price_index, finish_price in data[
                        'finish_and_design_prices'].iterrows():

                    if finish_price['Parameter2'] == 'CH' and finish_price[
                            'Parameter1'] == finish['HelmetFinishSKU']:
                        price_eur += float(finish_price['M2PriceEUR'])
                        price_usd += float(finish_price['M2PriceUSD'])
                        price_rmb += float(finish_price['M2PriceRMB'])
                    if finish_price['Parameter1'] == 'CH' and finish_price[
                            'Parameter2'] == design['Mark2PriceCategory']:
                        price_eur += float(finish_price['M2PriceEUR'])
                        price_usd += float(finish_price['M2PriceUSD'])
                        price_rmb += float(finish_price['M2PriceRMB'])
                # Boucler sur touts les items
                for item_index, item in data['helmet_items'].iterrows():
                    if item['FamilySKU'] == 'M2':
                        if item['ItemSKU'] == 'CH':
                            product = {
                                'Product_Code':
                                concat_sku([
                                    item['SKU'],
                                    design['DesignSKU'],
                                    finish['HelmetFinishSKU'],
                                ]),
                                'Description_EN':
                                concat_description([
                                    item['Family'],
                                    item['Helmet_Configuration_or_accesori'],
                                    design['DesignDescription'],
                                    finish['HelmetFinishDescription'],
                                ]),
                                'SD_EN':
                                concat_description([
                                    item['Family'],
                                    item['Helmet_Configuration_or_accesori'],
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
                                float(item['EUR']) + price_eur,
                                'USD':
                                float(item['USD']) + price_usd,
                                'RMB':
                                float(item['RMB']) + price_rmb,
                                'description_FRlong':
                                concat_description([
                                    item['Description_FR'],
                                    design['Description_FR'],
                                ]),
                                'description_ESlong':
                                concat_description([
                                    item['Description_ES'],
                                    design['Description_ES'],
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
                                'Collection':
                                design['Collection'],
                                'Finition':
                                finish['HelmetFinishSKU'],
                            }
                            products.append(product)

    data_frame = pd.DataFrame(products)
    sheet = gc.open_by_url(database)
    worksheet = sheet.worksheet('MK2CH')
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
