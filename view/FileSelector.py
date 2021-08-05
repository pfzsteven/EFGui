from PyQt5 import QtWidgets


def openDirectory():
    result = QtWidgets.QFileDialog.getExistingDirectory()
    return result


def openFile(dir):
    fd = QtWidgets.QFileDialog()
    fd.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
    return fd.getSaveFileName(directory=dir)
