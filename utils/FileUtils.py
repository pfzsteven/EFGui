import os
import shutil
from pathlib import Path


def createNewFile(path):
    file = Path(path)
    file.touch()


def createNewDir(path):
    os.mkdir(path)
    pass


def isFileExists(path):
    return os.path.exists(path)


def deleteDir(path):
    shutil.rmtree(path)


def deleteFile(path):
    if os.path.exists(path):
        # 判断是否为文件夹
        (_, ext) = os.path.splitext(path)
        if len(ext) == 0:
            shutil.rmtree(path)
            pass
        else:
            os.remove(path)
            pass
        pass
    pass


def writeString2File(path, text):
    file = open(path, mode='w+')
    file.write(text)
    file.close()
