import json
import shutil
from datetime import datetime

from pyunpack import Archive
import bz2
import requests
import os

IsFullCheck = False
ETCconstant = 9.5e-08

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


def download_file(url, file, path, fastdl_path, tree):
    contents = []
    print(tree)

    for i in tree:
        if i.rsplit('.')[-1] == 'bsp'  or i.rsplit('.')[-1] == 'nav':
            contents.append(i)
        else:
            return

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
    addToFastdl(path + "/" + i, os.path.join(fastdl_path, "{}.bz2".format(fastdl_path + "/" + i)))
    os.remove(file)


def switch(arg):
    cases = {
        "rar": "",
        "zip": "",
        "tar": "",
    }

    return cases.get(arg, "Unknown file format.")

def bz2Compress(rootfile, fdfile):
    print("Compressing {}, ETC: {:.2f} seconds...".format(rootfile, os.path.getsize(rootfile) * ETCconstant))
    with open(rootfile, "rb") as inp, bz2.BZ2File(fdfile, "wb", compresslevel = 1) as out:
        shutil.copyfileobj(inp, out)

def addToFastdl(rootfile, fdfile, copy = False):
	global TotalFilesUpdated, TotalFilesChanged, TotalFilesRemoved
	
	if not os.path.exists(fdfile):
		print("Adding {} to fastdl...".format(rootfile))
		if copy:
			shutil.copyfile(rootfile, fdfile)
		else:
			bz2Compress(rootfile, fdfile)
	elif IsFullCheck:
		if copy:
			if os.path.getsize(fdfile) != os.path.getsize(rootfile) or not filesEqual(rootfile, fdfile):
				print("Found changed file {}, replacing...".format(rootfile))
				shutil.copyfile(rootfile, fdfile)
		else:
			if not filesEqual(rootfile, fdfile, True):
				print("Found changed file {}, replacing...".format(rootfile))
				bz2Compress(rootfile, fdfile)
