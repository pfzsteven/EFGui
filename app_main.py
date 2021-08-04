import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileSystemModel

import FileNames
from main_editor import Ui_Dialog
from view import ClickEvent, FileSelector

currentWorkProject = None


def isWorkProjectSet():
    return currentWorkProject is not None


def openProject():
    # 展示文件弹窗
    global currentWorkProject
    currentWorkProject = FileSelector.openDirectory()
    global ui_dialog
    treeMode = QFileSystemModel()
    treeMode.setRootPath(currentWorkProject)
    ui_dialog.treeView.setModel(treeMode)
    pass


def initProject():
    os.open(FileNames.FILE_LOCALLY_JSON, "w")
    pass


def initWidgets():
    global ui_dialog
    # open project button
    ClickEvent.setOnClickListener(ui_dialog.btn_open_proj, openProject)
    # init project files
    ClickEvent.setOnClickListener(ui_dialog.btn_init, initProject)
    pass

pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui_dialog = Ui_Dialog()
    ui_dialog.setupUi(form)
    initWidgets()
    form.show()
    sys.exit(app.exec_())
