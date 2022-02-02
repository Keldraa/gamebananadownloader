import json
from shutil import copyfileobj, copyfile, move, rmtree
from datetime import datetime
from pyunpack import Archive
import bz2
from requests import get
import os
from time import time
from sys import argv
import ftplib

IsFullCheck = False
ETCconstant = 9.5e-08
cmpReadSize = 128000

with open("config.yml", "r") as file:
    cfg = yaml.safe_load(file)

#TODO: check for file formats (zip, rar, tar)
#TODO: check if directories exist inside unzipped file

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

        valid_files, failed = check_extensions("./temp")

        for i in valid_files:
            #prevent duplicates
            if os.path.isfile("./temp/" + i):
                move("./temp/" + i, path)
            else:
                continue

    rmtree("./temp")
    addToFastdl(path + "/" + i, os.path.join(fastdl_path,
                "{}.bz2".format(fastdl_path + "/" + i)))
    os.remove(file)

def bz2Compress(rootfile, fdfile):
    print("Compressing {}, ETC: {:.2f} seconds...".format(
        rootfile, os.path.getsize(rootfile) * ETCconstant))
    with open(rootfile, "rb") as inp, bz2.BZ2File(fdfile, "wb", compresslevel=1) as out:
        copyfileobj(inp, out)


def addToFastdl(rootfile, fdfile, copy=False):
    global TotalFilesUpdated, TotalFilesChanged, TotalFilesRemoved

    env = cfg['ftp']

    if not os.path.exists(fdfile):
        print(f"Adding {rootfile} to fastdl...")
        if copy:
            copyfile(rootfile, fdfile)
        else:
            bz2Compress(rootfile, fdfile)
    elif IsFullCheck:
        if copy:
            if os.path.getsize(fdfile) != os.path.getsize(rootfile) or not filesEqual(rootfile, fdfile):
                print(f"Found changed file {rootfile}, replacing...")
                copyfile(rootfile, fdfile)
        else:
            if not filesEqual(rootfile, fdfile, True):
                print(f"Found changed file {rootfile}, replacing...")
                bz2Compress(rootfile, fdfile)


    #storlines() for text files 
    #storbinary() for other files

    with FTP(
        env['host'],
        env['user'],
        env['pass'],
        env['port'], wdir) as ftp, open(fdfile, 'rb') as file:
        ftp.cwdr(fdfile.rsplit("/", 1)[:-1][0])
        ftp.storbinary(f'STOR {fdfile}', file)

def check_extensions(wdir, game):

    subfolders = [f.path for f in os.scandir(wdir) if f.is_dir()]
    folders = ['maps', 'materials', 'sound']


    #TODO: not sure if these work, never been tested and need further checking
    for i in subfolders:
        if not i in folders:
            for f in os.listdir(i):
                src = os.path.join(sub, f)
                dst = os.path.join(wdir, f)
                shutil.move(src, dst)
        else:
            for f in os.listdir(i):
                shutil.move(f, cases.get(i)) 

    checked = []
    failed = 0

    #TODO: not done (check top)

    for i in os.listdir(wdir):
        #place it in the correct path if it's not a directory and has a valid extension
        if not os.isdir(i):    
            if i.rsplit('.')[-1] in cfg['valid_formats']:
                checked.append(i)
        else:
            failed += 1
    return checked, failed

def switch(args):
    cases = {
        'materials': cfg['paths']+'/materials',
        'maps': cfg['paths']+'maps',
        'sound': cfg['paths']+'sound'
    }
    return cases.get(args, "Unknown")
