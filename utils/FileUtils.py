import os
import shutil


def createNewFile(path):
    fd = os.open(path, flags=os.O_RDWR)
    os.write(fd, b"")
    os.close(fd)


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
    fd = os.open(path, flags=os.O_RDWR)
    os.write(fd, bytes(text, encoding='utf-8'))
    os.close(fd)
