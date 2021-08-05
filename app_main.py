import json
import ntpath
import os
import sys

import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu

from main_editor import Ui_Dialog
from submodel.locally.subEditorGui import LocallyFileEditor, SimpleEditor, GogogoEditor
from utils import FileUtils, FileNames, ToastUtils
from view import ClickListener, FileSelector

# 当前工作路径
currentWorkProject: str = None

text_cache = {}


def isWorkProjectSet():
    return currentWorkProject is not None


def openProject():
    # 展示文件弹窗
    global currentWorkProject
    currentWorkProject = FileSelector.openDirectory()
    if not currentWorkProject.endswith("/"):
        currentWorkProject = currentWorkProject + "/"
        pass
    print("currentWorkProject = %s" % currentWorkProject)
    global explorerModel
    explorerModel = QtWidgets.QFileSystemModel()
    explorerModel.setRootPath(currentWorkProject)
    ui_dialog.treeView.setModel(explorerModel)
    model_index = explorerModel.index(currentWorkProject)
    ui_dialog.treeView.setRootIndex(model_index)

    for i in range(1, explorerModel.columnCount()):
        ui_dialog.treeView.hideColumn(i)
        pass
    checkLocallyJson()
    pass


def checkLocallyJson():
    if not os.path.exists(currentWorkProject):
        return
    locally_json_path = currentWorkProject + FileNames.FILE_LOCALLY_JSON
    new_string = file2String(locally_json_path)
    # 检查文件夹完整性
    if len(new_string) > 0:
        j = json.loads(new_string)
        items = j["item"]
        filterIds = []
        for item in items:
            # 滤镜id
            filter_id = item["id"]
            filterIds.append(filter_id)
            exists = os.path.exists(currentWorkProject + filter_id)
            if exists is False:
                # 创建新滤镜文件夹
                dir_path = currentWorkProject + filter_id
                FileUtils.createNewDir(dir_path)
                # 创建gogogo脚本文件
                FileUtils.createNewFile(dir_path + "/" + FileNames.FILE_SCRIPT_TEXT)
                FileUtils.createNewFile(dir_path + "/" + FileNames.FILE_SCRIPT_BACK_TEXT)
                # 创建config.json
                FileUtils.createNewFile(dir_path + "/" + FileNames.FILE_CONFIG_JSON)
                pass
            pass
        # 根目录
        sub_files = os.listdir(currentWorkProject)
        to_delete_files = []
        for f_path in sub_files:
            (_, ext) = os.path.splitext(f_path)
            if len(ext) == 0:
                f_name = ntpath.basename(f_path)
                if filterIds.count(f_name) == 0:
                    to_delete_files.append(f_path)
                    pass
                else:
                    filterIds.remove(f_name)
                    pass
                pass
            pass
        pass
        print("to delete invalid dirs %d " % len(to_delete_files))
        print("filterIds remains count:%d " % (len(filterIds)))
        for delete_path in to_delete_files:
            print("to delete file %s" % delete_path)
            FileUtils.deleteFile(delete_path)
            pass
        pass
    # 刷新控件
    refreshTreeView()
    pass


def refreshTreeView():
    explorerModel.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())


def initProject():
    if currentWorkProject is None:
        ToastUtils.warn('提示', "请先打开工程")
        return
    pass
    json_path = currentWorkProject + FileNames.FILE_LOCALLY_JSON
    if not FileUtils.isFileExists(json_path):
        FileUtils.createNewFile(json_path)
        pass
    else:
        ToastUtils.warn('提示', FileNames.FILE_LOCALLY_JSON + "文件已存在")
    pass


def showText(text):
    text_view.setText(text)
    pass


def file2String(path):
    cache = text_cache.get(path, None)
    if cache is not None:
        return cache
    with open(path) as f:
        data = f.read()
        f.close()
        pass
    text_cache[path] = data
    return data


def onTreeViewSingleClick(qmodelIndex):
    """单击事件回调"""
    path = explorerModel.filePath(qmodelIndex)
    (_, ext) = os.path.splitext(path)
    (parent, file_name) = os.path.split(path)

    # print("click file parent %s" % parent)
    # print("click file name %s" % file_name)
    # print("click file ext %d" % len(ext))

    if file_name.count("png") > 0 or len(ext) == 0 or file_name.count(".") == 0:
        showText("")
        pass
    else:
        showText((file2String(path)))
        pass
    pass


def onEditComplete(file_path, new_string):
    """编辑文本完成后回调"""
    text_cache[file_path] = new_string
    showText(new_string)
    pass


def onEditLocallyJsonComplete(file_path, new_string):
    """编辑Locally.json文本完成后回调"""
    text_cache[file_path] = new_string
    showText(new_string)
    # 初始化创建文件夹或者删除文件夹
    checkLocallyJson()
    pass


def onTreeViewDoubleClick(qmodelIndex):
    """双击事件回调"""
    path = explorerModel.filePath(qmodelIndex)
    (_, ext) = os.path.splitext(path)
    (parent, file_name) = os.path.split(path)

    # print("double click file parent %s" % parent)
    # print("double click file name %s" % file_name)
    # print("double click file ext %d" % len(ext))

    if file_name.count("png") > 0 or len(ext) == 0 or file_name.count(".") == 0:
        pass
    else:
        if file_name == FileNames.FILE_LOCALLY_JSON:
            LocallyFileEditor().show(file_path=path, json_str=file2String(path), callback=onEditLocallyJsonComplete)
        elif file_name == FileNames.FILE_SCRIPT_TEXT or file_name == FileNames.FILE_SCRIPT_BACK_TEXT:
            GogogoEditor().show(file_path=path, json_str=file2String(path), callback=onEditComplete)
            pass
        else:
            if file_name.count("png") > 0:
                pass
            else:
                SimpleEditor().show(file_path=path, json_str=file2String(path), callback=onEditComplete)
                pass
            pass
        pass


def create_new_file(event):
    selectionModel = ui_dialog.treeView.currentIndex()
    path = explorerModel.filePath(selectionModel)
    file_path = FileSelector.openFile(path)
    FileUtils.createNewFile(file_path[0])
    refreshTreeView()
    return True


def delete_file(event):
    selectionModel = ui_dialog.treeView.currentIndex()
    path = explorerModel.filePath(selectionModel)
    FileUtils.deleteFile(path)
    refreshTreeView()
    return True


def show_context_menu(pos: PyQt5.QtCore.QPoint):
    modelIndex: QModelIndex = ui_dialog.treeView.indexAt(pos)
    path = explorerModel.filePath(modelIndex)
    (_, ext) = os.path.splitext(path)

    menu = QMenu()
    if len(ext) == 0:  # it's a dir type
        create_new_file_action = menu.addAction('新建')
        create_new_file_action.triggered.connect(create_new_file)
        menu.addSeparator()
        pass
    delete_file_action = menu.addAction('删除')
    delete_file_action.triggered.connect(delete_file)
    menu.exec_(QCursor.pos())
    pass


def initTreeView():
    ui_dialog.treeView.clicked.connect(onTreeViewSingleClick)
    ui_dialog.treeView.doubleClicked.connect(onTreeViewDoubleClick)
    ui_dialog.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
    ui_dialog.treeView.customContextMenuRequested.connect(show_context_menu)
    pass


def initWidgets():
    initTreeView()
    global ui_dialog
    # open project button
    ClickListener.setOnClickListener(ui_dialog.btn_open_proj, openProject)
    # init project files
    ClickListener.setOnClickListener(ui_dialog.btn_init, initProject)
    pass


pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui_dialog = Ui_Dialog()
    ui_dialog.setupUi(form)

    text_view = QtWidgets.QLabel()
    text_view.setWordWrap(True)
    ui_dialog.scrollArea.setWidget(text_view)
    initWidgets()
    form.show()
    sys.exit(app.exec_())
