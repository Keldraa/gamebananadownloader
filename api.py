import json
import shutil
from datetime import datetime

from pyunpack import Archive
import requests
import os


class GamebananaAPI:
    def __init__(self, mod_id):
        self.base_api = "https://gamebanana.com/apiv7/Mod/" + str(
            mod_id) + "?_csvProperties=_idRow,_sName,_aFiles,_aGame,_sName,_aPreviewMedia,_aSubmitter&_csvFlags=FILE_METADATA"

    def get_json(self):
        try:
            r = requests.get(self.base_api)
            j = json.loads(r.content)
            return j
        except:
            return []


def get_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)

    return dt_object


def download_file(url, file, path, tree):
    contents = []

    for i in tree:
        if (not i.rsplit('.')[-1] == 'bsp') or (not i.rsplit('.')[-1] == 'nav'):
            pass
        else:
            contents.append(i)

    if not os.path.isdir("./temp"):
        os.mkdir("./temp")

    with requests.get(url, stream=True) as r:
        with open(file, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        Archive(file).extractall("./temp")

        for i in contents:
            if os.path.isfile("./temp/" + i):
                shutil.move("./temp/" + i, path)
            else:
                pass

    shutil.rmtree("./temp")
    os.remove(file)
