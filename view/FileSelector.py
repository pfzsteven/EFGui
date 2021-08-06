from PyQt5 import QtWidgets


def openDirectory():
    result = QtWidgets.QFileDialog.getExistingDirectory()
    return result


def openSaveDirectory():
    fd = QtWidgets.QFileDialog()
    fd.setFileMode(QtWidgets.QFileDialog.FileMode.DirectoryOnly)
    path = fd.getSaveFileName()
    if path is tuple:
        return path[0]
    else:
        return path


def openFile(dir):
    fd = QtWidgets.QFileDialog()
    fd.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
    return fd.getSaveFileName(directory=dir)


def openAnyFile():
    fd = QtWidgets.QFileDialog()
    return fd.getOpenFileName()
