from PyQt5 import QtWidgets


def openDirectory():
    result = QtWidgets.QFileDialog.getExistingDirectory()
    return result
