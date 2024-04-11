import pandas as pd
from data import database, get_data, gc
from utils import concat_sku, concat_description


def generate_parents():

    products = []
    data = get_data()

    # Boucler sur tous les designs
    for design_index, design in data['designs'].iterrows():
        percent_done = round((design_index + 1) / len(data['designs']) * 100)
        print("Progression ", percent_done, "%")

        # Boucler sur toutes les finitions
        for finish_index, finish in data['helmet_finishes'].iterrows():

            # Si le design correspond à la finition
            if design['HelmetFinishes'] == finish['HelmetFinish']:

                # Boucler sur toutes les configurations
                for config_index, config in data['helmet_config'].iterrows():

                    # Si le design correspond à la config
                    if design['Mark1Config'] == config['Mark1Config']:

                        # Boucler sur tous les items
                        for item_index, item in data['helmet_items'].iterrows(
                        ):

                            if item['FamilySKU'] == 'M1':
                                if item['ItemSKU'] == config['Mark1ConfigSKU']:
                                    product = {
                                        'Product_Code':
                                        concat_sku(
                                            [item['SKU'],
                                             design['DesignSKU']]),
                                        'Description_EN':
                                        concat_description([
                                            item['Family'], item[
                                                'Helmet_Configuration_or_accesori'],
                                            design['DesignDescription']
                                        ]),
                                        'description_FR':
                                        concat_description([
                                            item['Family'], item['SD_FR'],
                                            design['DesignDescription']
                                        ]),
                                        'description_ENlong':
                                        concat_description([
                                            item['Description_EN'],
                                            design['Description_EN']
                                        ]),
                                        'description_CNlong':
                                        concat_description([
                                            item['Description_CN'],
                                            design['Description_CN']
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
    worksheet = sheet.worksheet('PARENTS')
    worksheet.clear()

    worksheet.update([data_frame.columns.values.tolist()] +
                     data_frame.values.tolist())
    print("Fini ! ", database)
