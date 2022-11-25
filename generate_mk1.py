import pandas as pd
import gspread as gs
from credentials import credentials
from data import database, sources
from utils import concat_sku, concat_description


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
        for certification_index, certification in data['mark1_certifications'].iterrows():

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
              for config_index, config in data[
                      'helmet_config'].iterrows():

                # Si le design correspond à la config
                if design['Mark1Config'] == config['Mark1Config']:
                  # Boucler sur touts les prix / finitions
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
  
                  # Boucler sur tous les items
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
                                        'FamilySKU':
                                        item['SKU'],
                                        'Certification':
                                        certification[
                                            'Mark1Certifications'],
                                        'Finition':
                                        finish['HelmetFinishSKU'],
                                        'Collection':
                                        design['Collection'],
                                    }
                                    products.append(product)

  data_frame = pd.DataFrame(products)
  sheet = gc.open_by_url(database)
  worksheet = sheet.worksheet('MK1')
  worksheet.clear()

  worksheet.update([data_frame.columns.values.tolist()] +
                   data_frame.values.tolist())
  print("Fini ! ", database)
