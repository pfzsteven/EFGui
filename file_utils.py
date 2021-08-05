import os
from pathlib import Path


def createNewFile(path):
    print("createNewFile...")
    print(path)
    file = Path(path)
    file.touch()


def deleteFile(path):
    print("deleteFile...")
    print(path)
    os.remove(path)
