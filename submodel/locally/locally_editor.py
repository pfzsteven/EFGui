import json

from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QDialog

from submodel.interfaces import BaseEditor
from submodel.locally.locally_table_view import LocallyTableModel
from utils import FileNames, FileUtils, ToastUtils


# locally.json 编辑
class LocallyFileEditor(BaseEditor):

    def __init__(self):
        super().__init__()
        self.version = ""

    def refresh(self):
        """
        刷新控件
        :return:
        """
        table_model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        pass

    def accept(self):
        ui_dialog.tableView.setCurrentIndex(QModelIndex())

        json_str = "{}"
        jsonObject = json.loads(json_str)
        if self.version is None or len(self.version) == 0:
            self.version = "1.0"
            pass
        pass
        jsonObject["version"] = self.version
        items = []
        error = False
        filter_ids = []
        for row in range(0, table_model.rowCount()):
            f_id = str(table_model.data(table_model.index(row, 1),
                                        role=(QtCore.Qt.DisplayRole or QtCore.Qt.EditRole)))
            if filter_ids.count(f_id):
                error = True
                break
                pass
            filter_ids.append(f_id)
            f_name = str(table_model.data(table_model.index(row, 2),
                                          role=(QtCore.Qt.DisplayRole or QtCore.Qt.EditRole)))
            makeup_id = str(table_model.data(table_model.index(row, 3),
                                             role=(QtCore.Qt.DisplayRole or QtCore.Qt.EditRole)))

            item = {}
            if len(f_id) > 0 and len(f_name) > 0:
                item["id"] = f_id.upper()
                item["name"] = f_name
                if makeup_id == "None":
                    item["makeup_id"] = ""
                    pass
                else:
                    item["makeup_id"] = makeup_id.upper()
                    pass
                pass
                # 合法数据
                items.append(item)
            elif len(f_id) > 0 or len(f_name) > 0:
                error = True
                break
            pass
        pass
        if not error:
            jsonObject["item"] = items
            new_json_str = json.dumps(jsonObject, ensure_ascii=False, indent=4)
            FileUtils.writeString2File(text=new_json_str, path=self.file_path)
            if self.callback is not None:
                self.callback(self.file_path, new_json_str)
            dialog.close()
            pass
        else:
            ToastUtils.warn(title="提示", msg="规则:滤镜ID不能重复,且滤镜名称均为必填项")
        pass

    def reject(self):
        dialog.close()
        pass

    def delete_row(self):
        """
        删除某一行数据
        :param pos:
        :return:
        """
        modelIndex = ui_dialog.tableView.currentIndex()
        if modelIndex is None:
            return
        table_model.clearRowData(modelIndex)
        self.refresh()
        pass

    def initTableView(self):
        ui_dialog.tableView.setModel(table_model)
        pass

    def show(self, file_path, text=None, callback=None):
        self.file_path = file_path
        self.callback = callback
        global ui_dialog
        global dialog
        from submodel.locally.locally_design import Ui_Dialog
        dialog = QDialog()
        ui_dialog = Ui_Dialog()
        ui_dialog.setupUi(dialog)
        # print("edit locally json:%s" % json_str)
        items = []
        j = json.loads(text)
        self.version = j["version"]
        json_array = j["item"]
        data_size = 0
        table_index = 1
        if json_array is not None:
            data_size = len(json_array)
            for item in json_array:
                row_data = [table_index, item["id"], item["name"], item.get("makeup_id")]
                # print(row_data)
                table_index += 1
                items.append(row_data)
                pass
        # 额外创建50行
        for c in range(0, 50 - data_size):
            items.append([table_index, "", "", ""])
            table_index += 1
            pass
        global table_model
        table_model = LocallyTableModel(data=items)
        self.initTableView()
        ui_dialog.buttonBox.accepted.connect(self.accept)
        ui_dialog.buttonBox.rejected.connect(self.reject)
        ui_dialog.btn_delete_row.clicked.connect(self.delete_row)
        dialog.setWindowTitle(FileNames.FILE_LOCALLY_JSON)
        dialog.exec()
        pass
