from dotenv import load_dotenv
import os
import sys
import shutil
from checksumdir import dirhash

user = os.getlogin()

def main():
    load_dotenv()
    global user
    init = os.path.exists(os.getenv(r"INIT_PATH").format(user))
    if (not init):
        syncDir = os.path.join(os.getenv(r"USER_PATH").format(user), "CloudSync")
        initDir = os.path.join(os.getenv(r"USER_PATH").format(user), ".sync")
        os.mkdir(syncDir)
        os.mkdir(initDir)
        print("initialized")

    testConnection()
        
def testConnection():
    connection = (lambda a: True if 0 == a.system(f'ping {os.getenv("IP_SERVER")} -w 4') else False)
    if (connection):
        envTarget = os.getenv("SERVER_PATH")
        shareAvailable = os.path.exists(envTarget)
    if (shareAvailable and sys.argv[1] == "down"):
        DownSync()
    if (shareAvailable and sys.argv[1] == "up"):
        UpSync()


def DownSync():
    global user
    src = os.getenv(r"SERVER_PATH").format(user)
    dst = os.getenv(r"LOCAL_PATH").format(user)
    if (os.path.exists(dst)):
        dirs = os.listdir(src)
        for dir in dirs:
            srcPath = f'{src}\\{dir}'
            localPath = f'{dst}\\{dir}'
            localDir = os.path.exists(localPath)
            if (not localDir):
                shutil.copytree(srcPath, localPath)
            else:
                if (compareHash(srcPath, localPath)):
                    continue
                shutil.rmtree(localPath)
                shutil.copytree(srcPath, localPath)

    else:
        shutil.copytree(src, dst)


def compareHash(srcPath, dstPath):
    try:
        if (dirhash(srcPath) == dirhash(dstPath)):
            return True
        return False
    except:
        return False


def UpSync():
    global user
    src = os.getenv(r"LOCAL_PATH").format(user)
    dst = os.getenv(r"SERVER_PATH").format(user)
    if (os.path.exists(dst)):
        dirs = os.listdir(src)
        for dir in dirs:
            srcPath = f'{src}\\{dir}'
            localPath = f'{dst}\\{dir}'
            localDir = os.path.exists(localPath)
            if (not localDir):
                shutil.copytree(srcPath, localPath)
            else:
                if (compareHash(srcPath, localPath)):
                    continue
                shutil.rmtree(localPath)
                shutil.copytree(srcPath, localPath)
    else:
        shutil.copytree(srcPath, localPath)

        
main()