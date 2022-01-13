import json
from shutil import copyfileobj, copyfile, move, rmtree
from datetime import datetime
from pyunpack import Archive
import bz2
from requests import get
import os
from time import time
from sys import argv

IsFullCheck = False
ETCconstant = 9.5e-08
cmpReadSize = 128000

class GamebananaAPI:
    def __init__(self, mod_id):
        self.base_api = "https://gamebanana.com/apiv7/Mod/" + str(
            mod_id) + "?_csvProperties=_idRow,_sName,_aFiles,_aGame,_sName,_aPreviewMedia,_aSubmitter&_csvFlags=FILE_METADATA"

    def get_json(self):
        try:
            r = get(self.base_api)
            j = json.loads(r.content)
            return j
        except:
            return []


def filesEqual(rootfile, fdfile, bz2format=False):
    prevtime = time()
    if bz2format:
        with open(rootfile, "rb") as inp, bz2.BZ2File(fdfile, "rb") as out:
            while True:
                p1 = inp.read(cmpReadSize)
                p2 = out.read(cmpReadSize)
                if p1 != p2:
                    print("BZ2 File {} compared for {:.2f} seconds".format(
                        rootfile, time() - prevtime))
                    return False
                if not p1:
                    print("BZ2 File {} compared for {:.2f} seconds".format(
                        rootfile, time() - prevtime))
                    return True
    else:
        with open(rootfile, "rb") as inp, open(fdfile, "rb") as out:
            while True:
                p1 = inp.read(cmpReadSize)
                p2 = out.read(cmpReadSize)
                if p1 != p2:
                    print("File {} compared for {:.2f} seconds".format(
                        rootfile, time() - prevtime))
                    return False
                if not p1:
                    print("File {} compared for {:.2f} seconds".format(
                        rootfile, time() - prevtime))
                    return True


def get_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)

    return dt_object


def download_file(url, file, path, fastdl_path, tree):
    contents = []
    print(tree)

    for i in tree:
        if i.rsplit('.')[-1] == 'bsp' or i.rsplit('.')[-1] == 'nav':
            contents.append(i)
        else:
            return

    if not os.path.isdir("./temp"):
        os.mkdir("./temp")

    with get(url, stream=True) as r:
        with open(file, 'wb') as f:
            copyfileobj(r.raw, f)

        Archive(file).extractall("./temp")

        for i in contents:
            if os.path.isfile("./temp/" + i):
                move("./temp/" + i, path)
            else:
                pass

    rmtree("./temp")
    addToFastdl(path + "/" + i, os.path.join(fastdl_path,
                "{}.bz2".format(fastdl_path + "/" + i)))
    os.remove(file)


def switch(arg):
    cases = {
        "rar": "",
        "zip": "",
        "tar": "",
    }

    return cases.get(arg, "Unknown file format.")


def bz2Compress(rootfile, fdfile):
    print("Compressing {}, ETC: {:.2f} seconds...".format(
        rootfile, os.path.getsize(rootfile) * ETCconstant))
    with open(rootfile, "rb") as inp, bz2.BZ2File(fdfile, "wb", compresslevel=1) as out:
        copyfileobj(inp, out)


def addToFastdl(rootfile, fdfile, copy=False):
    global TotalFilesUpdated, TotalFilesChanged, TotalFilesRemoved

    if not os.path.exists(fdfile):
        print("Adding {} to fastdl...".format(rootfile))
        if copy:
            copyfile(rootfile, fdfile)
        else:
            bz2Compress(rootfile, fdfile)
    elif IsFullCheck:
        if copy:
            if os.path.getsize(fdfile) != os.path.getsize(rootfile) or not filesEqual(rootfile, fdfile):
                print("Found changed file {}, replacing...".format(rootfile))
                copyfile(rootfile, fdfile)
        else:
            if not filesEqual(rootfile, fdfile, True):
                print("Found changed file {}, replacing...".format(rootfile))
                bz2Compress(rootfile, fdfile)
