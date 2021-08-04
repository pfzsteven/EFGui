import os
import sys

from PyQt5 import QtWidgets

import FileNames
from main_editor import Ui_Dialog
from submodel.subEditorGui import LocallyFileEditor
from view import ClickEvent, FileSelector

# 当前工作路径
currentWorkProject = None


def isWorkProjectSet():
    return currentWorkProject is not None


def openProject():
    # 展示文件弹窗
    global currentWorkProject
    currentWorkProject = FileSelector.openDirectory() + "/"
    global explorerModel
    explorerModel = QtWidgets.QFileSystemModel()
    explorerModel.setRootPath(currentWorkProject)
    ui_dialog.treeView.setModel(explorerModel)
    model_index = explorerModel.index(currentWorkProject)
    ui_dialog.treeView.setRootIndex(model_index)

    for i in range(1, explorerModel.columnCount()):
        ui_dialog.treeView.hideColumn(i)
        pass

    pass


def initProject():
    os.open(FileNames.FILE_LOCALLY_JSON, os.O_WRONLY)
    pass


def file2Json(path):
    with open(path) as f:
        data = f.read()
        f.close()
    return data
    pass


def onTreeViewDoubleClick(qmodelIndex):
    path = explorerModel.filePath(qmodelIndex)
    (_, ext) = os.path.splitext(path)
    (parent, file_name) = os.path.split(path)
    print("click file parent %s" % parent)
    print("click file name %s" % file_name)
    if file_name == FileNames.FILE_LOCALLY_JSON:
        LocallyFileEditor().show(file2Json(path))
    pass


def initTreeView():
    ui_dialog.treeView.doubleClicked.connect(onTreeViewDoubleClick)
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
