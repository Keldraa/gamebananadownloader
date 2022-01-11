import json
import shutil
from datetime import datetime

from pyunpack import Archive
import bz2
import requests
import os


class GamebananaAPI:
    def __init__(self, mod_id):
        self.base_api = "https://gamebanana.com/apiv5/Mod/" + str(
            mod_id) + "?_csvProperties=_idRow,_sName,_aFiles,_aGame,_sName,_aPreviewMedia,_aSubmitter"

    def get_json(self):
        url = self.base_api
        try:
            r = requests.get(self.base_api)
            j = json.loads(r.content)
            return j
        except:
            return []


def get_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)

    return dt_object


def download_file(url, file, path, name):
    with requests.get(url, stream=True) as r:
        with open(file, 'wb') as f:
            print(path)
            shutil.copyfileobj(r.raw, f)
        Archive(file).extractall(path)
    os.remove(file)
