import os
from pathlib import Path


def createNewFile(path):
    file = Path(path)
    file.touch()


def deleteFile(path):
    if os.path.exists(path):
        os.remove(path)


def writeString2File(text: str, path: str):
    file = open(path, mode='w+')
    file.write(text)
    file.flush()
    file.close()
