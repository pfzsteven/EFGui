import json
import ntpath
import os
import re
import sys
from pathlib import Path

import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu

from main_editor import Ui_Dialog
from submodel.gogogo.gogogo_editor_gui import GogogoEditor
from submodel.locally.locally_editor_gui import LocallyFileEditor
from submodel.simple.simple_text_editor import SimpleEditor
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
    if len(currentWorkProject) == 0:
        return
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


def validateFiles():
    """
    校验当前内容
    :return:
    """
    pass


def validateJsonFiles(filter_id_dir: str, array):
    """
    校验json内容
    :param filter_id_dir: 滤镜文件夹路径
    :return:
    """
    if not FileUtils.isFileExists(filter_id_dir):
        return

    (_, file_name) = os.path.split(filter_id_dir)

    files = [f for f in os.listdir(filter_id_dir) if re.match(r'.*\.json', f)]
    # 检查 xxx.json，以及 ["icon.png", "script.txt", "script_config.json"] 文件是否存在
    icon_file = filter_id_dir + "/" + FileNames.FILE_ICON
    script_text = filter_id_dir + "/" + FileNames.FILE_SCRIPT_TEXT
    script_config_json = filter_id_dir + "/" + FileNames.FILE_SCRIPT_CONFIG_JSON

    if not FileUtils.isFileExists(icon_file):
        array.append(file_name + "缺失文件 " + FileNames.FILE_ICON)

    if not FileUtils.isFileExists(script_text):
        array.append(file_name + "缺失文件 " + FileNames.FILE_SCRIPT_TEXT)

    if not FileUtils.isFileExists(script_config_json):
        array.append(file_name + "缺失文件 " + FileNames.FILE_SCRIPT_CONFIG_JSON)
    pass

    for file in files:
        path = filter_id_dir + "/" + file
        (_, j_file_name) = os.path.split(path)
        json_string = file2String(path, addInCache=False)
        try:
            json.loads(json_string)
        except Exception as e:
            print(e)
            array.append(file_name + "/" + j_file_name + " 发生json错误")
            pass


def searchLocallyParentDir(parent):
    locally_json_file = parent + "/" + FileNames.FILE_LOCALLY_JSON
    if FileUtils.isFileExists(locally_json_file):
        print("yes , i find it #1. return %s" % parent)
        return parent
    result = None
    for sub_file in os.listdir(parent):
        if result is not None:
            break
        if sub_file.count(".") == 0:
            result = searchLocallyParentDir(parent + "/" + sub_file)
        else:
            if sub_file == FileNames.FILE_LOCALLY_JSON:
                result = parent
                print("yes , i find it #2. return %s" % parent)
        if result is not None:
            break
    return result


def validate(dir, validZip: False):
    root = dir
    if validZip:
        root = searchLocallyParentDir(dir)
        pass
    if root is None:
        print("sorry , can't find the root dir")
        return

    if FileUtils.isFileExists(root):
        (parent_dir, file_name) = os.path.split(root)
        valid_zip_error_log = []
        # 判断当前是否符合 Fxx 文件夹名称
        res = re.search("^F\\d+$", file_name)
        if res:
            validateJsonFiles(root, valid_zip_error_log)
            pass
        else:
            sub_files = os.listdir(root)
            # 检查 xxx.json，以及 ["icon.png", "script.txt", "script_config.json"] 文件是否存在
            for sub_file_name in sub_files:
                res = re.search("^F\\d+$", sub_file_name)
                if res:
                    validateJsonFiles(root + "/" + sub_file_name, valid_zip_error_log)
                    pass
                pass
            pass

        if len(valid_zip_error_log) > 0:
            error_msg = ""
            for elem in valid_zip_error_log:
                error_msg = error_msg + str(elem) + "\n"
                pass
            pass
            ToastUtils.warn(title="错误提示", msg=error_msg)
    pass


def exportZip():
    """
    导出为zip包
    :return:
    """
    validate(currentWorkProject)
    pass


def chooseZip2Validate():
    """
    选择zip包进行校验
    :return:
    """
    (path_to_zip_file, _) = FileSelector.openFile()
    if len(path_to_zip_file) > 0 and path_to_zip_file.count(".zip") > 0:
        (parent_dir, file_name) = os.path.split(path_to_zip_file)
        directory_to_extract_to = parent_dir + "/" + (file_name.replace(".zip", "") + "_tmp")
        # 删除旧的
        FileUtils.deleteFile(directory_to_extract_to)
        import zipfile
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
            pass
        validate(directory_to_extract_to, validZip=True)
    pass


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


def file2String(path, addInCache: bool = True):
    cache = text_cache.get(path, None)
    if cache is not None:
        return cache
    with open(path) as f:
        data = f.read()
        f.close()
        pass
    if addInCache:
        text_cache[path] = data
        pass
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


def createScriptText(parent, version, gen_back: bool):
    """
    创建脚本文件
    :param parent: 父路径
    :param version: 系统版本
    :param gen_back: 是否生成后置
    :return:
    """
    script_text = parent + "/" + "script_iphone" + version + ".txt"
    FileUtils.createNewFile(script_text)
    if gen_back is True:
        script_text_back = parent + "/" + "script_iphone" + version + "_back.txt"
        FileUtils.createNewFile(script_text_back)
        pass
    pass


def createScriptConfig(parent: str, gen_back: bool):
    """
    创建script_config.json文件
    :param parent: 父路径
    :param gen_back: 是否生成后置
    :return:
    """
    script_config_file_path = parent + "/" + FileNames.FILE_SCRIPT_CONFIG_JSON
    FileUtils.writeString2File(path=script_config_file_path, text="{}")
    if gen_back is True:
        script_config_back_file_path = parent + "/" + FileNames.FILE_SCRIPT_BACK_CONFIG_JSON
        FileUtils.writeString2File(path=script_config_back_file_path, text="{}")
        pass
    pass


def onGogogoScriptEditComplete(file_path: str, new_string: str, tube_gen_checked: tuple, tube_device_checked: tuple):
    """
    gogogo脚本编辑完成回调
    :param file_path: 文件路径
    :param new_string: 内容
    :param tube_gen_checked: [是否生成前后置脚本 or 是否仅生成前置脚本 or 是否仅生成后置脚本]
    :param tube_device_checked: 机型适配勾选列表：[iphone6,iphone8,iphoneX,iphone11,iphone12]
    :return:
    """
    text_cache[file_path] = new_string
    showText(new_string)
    parent_path = str(Path(file_path).parent.absolute())

    print("onGogogoScriptEditComplete %s " % parent_path)

    # 创建 script_config.json文件
    createScriptConfig(parent_path, tube_gen_checked[0] or tube_gen_checked[2])

    # iphone6
    if tube_device_checked[0] is True:
        createScriptText(parent_path, "6", tube_device_checked[0])
        pass
    # iphone8
    if tube_device_checked[1] is True:
        createScriptText(parent_path, "8", tube_device_checked[1])
        pass
    # iphonex
    if tube_device_checked[2] is True:
        createScriptText(parent_path, "x", tube_device_checked[2])
        pass
    # iphone11
    if tube_device_checked[3] is True:
        createScriptText(parent_path, "11", tube_device_checked[3])
        pass
    # iphone12
    if tube_device_checked[4] is True:
        createScriptText(parent_path, "12", tube_device_checked[4])
        pass
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
            LocallyFileEditor().show(file_path=path, text=file2String(path), callback=onEditLocallyJsonComplete)
        elif file_name == FileNames.FILE_SCRIPT_TEXT or file_name == FileNames.FILE_SCRIPT_BACK_TEXT:
            GogogoEditor().show(file_path=path, text=file2String(path), callback=onGogogoScriptEditComplete)
            pass
        else:
            if file_name.count("png") > 0:
                pass
            else:
                SimpleEditor().show(file_path=path, text=file2String(path), callback=onEditComplete)
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


def validate_current_dir(event):
    selectionModel = ui_dialog.treeView.currentIndex()
    path = explorerModel.filePath(selectionModel)
    validate(path)
    pass


def show_context_menu(pos: PyQt5.QtCore.QPoint):
    modelIndex: QModelIndex = ui_dialog.treeView.indexAt(pos)
    path = explorerModel.filePath(modelIndex)
    (_, ext) = os.path.splitext(path)

    menu = QMenu()
    if len(ext) == 0:  # it's a dir type
        validate_action = menu.addAction('校验当前文件夹')
        validate_action.triggered.connect(validate_current_dir)
        menu.addSeparator()

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
    # 校验
    ClickListener.setOnClickListener(ui_dialog.btn_validate, validateFiles)
    # 导出zip
    ClickListener.setOnClickListener(ui_dialog.btn_export_zip, exportZip)
    # 选择zip校验
    ClickListener.setOnClickListener(ui_dialog.btn_select_zip_validate, chooseZip2Validate)
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
