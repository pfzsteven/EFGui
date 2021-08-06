import os
import shutil
from pathlib import Path


def createNewFile(path):
    Path(path).touch()
    pass


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
    deleteFile(path)
    createNewFile(path)
    fd = os.open(path, flags=os.O_WRONLY)
    os.write(fd, bytes(text, encoding='utf-8'))
    os.close(fd)


def getFileName(path):
    (_, file_name) = os.path.split(path)
    return file_name


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
            pass
        pass
    pass


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
