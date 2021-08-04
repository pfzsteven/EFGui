import json
import os
import sys

from PyQt5 import QtWidgets

import FileNames
from main_editor import Ui_Dialog
from submodel.subEditorGui import LocallyFileEditor, SimpleEditor, GogogoEditor
from view import ClickEvent, FileSelector

# 当前工作路径
currentWorkProject = None

text_cache = json.loads("{}")


def isWorkProjectSet():
    return currentWorkProject is not None


def openProject():
    # 展示文件弹窗
    global currentWorkProject
    currentWorkProject = FileSelector.openDirectory()
    if not currentWorkProject.endswith("/"):
        currentWorkProject = currentWorkProject + "/"
        pass
    pass
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


def file2String(path):
    cache = text_cache.get(path)
    if cache is not None:
        return cache
    with open(path) as f:
        data = f.read()
        f.close()
        pass
    text_cache[path] = data
    return data


def onTreeViewSingleClick(qmodelIndex):
    path = explorerModel.filePath(qmodelIndex)
    (_, ext) = os.path.splitext(path)
    (parent, file_name) = os.path.split(path)
    print("click file parent %s" % parent)
    print("click file name %s" % file_name)
    print("click file ext %d" % len(ext))

    if file_name.count("png") > 0 or len(ext) == 0 or file_name.count(".") == 0:
        text_view.setText("")
        pass
    else:
        text_view.setText((file2String(path)))
        pass
    pass


def onTreeViewDoubleClick(qmodelIndex):
    path = explorerModel.filePath(qmodelIndex)
    (_, ext) = os.path.splitext(path)
    (parent, file_name) = os.path.split(path)
    print("double click file parent %s" % parent)
    print("double click file name %s" % file_name)
    print("double click file ext %d" % len(ext))

    if file_name.count("png") > 0 or len(ext) == 0 or file_name.count(".") == 0:
        pass
    else:
        if file_name == FileNames.FILE_LOCALLY_JSON:
            LocallyFileEditor().show(file2String(path))
        elif file_name == FileNames.FILE_SCRIPT_TEXT or file_name == FileNames.FILE_SCRIPT_BACK_TEXT:
            GogogoEditor().show(file2String(path))
            pass
        else:
            if file_name.count("png") > 0:
                pass
            else:
                SimpleEditor().show(file2String(path))
                pass
            pass
        pass


def initTreeView():
    ui_dialog.treeView.clicked.connect(onTreeViewSingleClick)
    ui_dialog.treeView.doubleClicked.connect(onTreeViewDoubleClick)
    # ui_dialog.treeView.contextMenuEvent.connect()
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

    text_view = QtWidgets.QLabel()
    ui_dialog.scrollArea.setWidget(text_view)
    initWidgets()
    form.show()
    sys.exit(app.exec_())
