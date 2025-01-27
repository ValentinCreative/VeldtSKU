import gspread as gs
from credentials import credentials
import pandas as pd

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
    'mark2_sizes':
    'https://docs.google.com/spreadsheets/d/1H4WHis3M0r7gbQXRkhOrx1L2s_uNgYi42SsFOR-ZFvo/edit#gid=1621514264',
}

gc = gs.service_account_from_dict(credentials)


def get_data(key=None):
    data = {}

    if key is not None:
        print("Récupération de la feuille ", key)
        sh = gc.open_by_url(database)
        ws = sh.worksheet(key)
        data = pd.DataFrame(ws.get_all_records())
    else:
        for key in sources:
            print("Récupération du fichier ", key)
            sh = gc.open_by_url(sources[key])
            ws = sh.get_worksheet(0)
            data[key] = pd.DataFrame(ws.get_all_records())

    return data
