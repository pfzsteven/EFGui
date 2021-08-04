import os
import sys

from PyQt5 import QtWidgets

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
    print("currentWorkProject %s" % currentWorkProject)
    global ui_dialog
    explorerModel = QtWidgets.QFileSystemModel()
    explorerModel.setRootPath(currentWorkProject)
    ui_dialog.treeView.setModel(explorerModel)
    model_index = explorerModel.index(os.path.dirname(currentWorkProject))
    ui_dialog.treeView.setRootIndex(model_index)

    for i in range(1, explorerModel.columnCount()):
        ui_dialog.treeView.hideColumn(i)
        pass

    pass


def initProject():
    os.open(FileNames.FILE_LOCALLY_JSON, os.O_WRONLY)
    pass


def initTreeView():
    pass


def initWidgets():
    initTreeView()
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
