import os
import json
import requests


class GamebananaAPI:
    def __init__(self, mod_id):
        self.base_api = "https://gamebanana.com/apiv5/Mod/" + str(mod_id) + "?_csvProperties=_idRow,_sName,_aFiles,_aGame,_sName,_aPreviewMedia,_aSubmitter"

    def get_json(self):
        url = self.base_api
        try:
            r = requests.get(self.base_api)
            j = json.loads(r.content)
            return j
        except:
            return []
