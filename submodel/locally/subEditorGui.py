import json
from abc import ABCMeta, abstractmethod

from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QDialog

import FileNames
from submodel.locally.locally_table_view import LocallyTableModel


class BaseEditor(metaclass=ABCMeta):

    @abstractmethod
    def show(self, json_str=None):
        pass


# locally.json 编辑
class LocallyFileEditor(BaseEditor):

    def __init__(self):
        self.version = ""

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

        for row in range(0, table_model.rowCount()):
            item = {}
            for col in range(1, table_model.columnCount()):
                value = str(
                    table_model.data(table_model.index(row, col),
                                     role=(QtCore.Qt.DisplayRole or QtCore.Qt.EditRole)))
                if col == 1:  # id
                    item["id"] = value
                    pass
                elif col == 2:  # name
                    item["name"] = value
                    pass
                elif col == 3:  # makeup_id
                    if value is None or str(value) == "None":
                        item["makeup_id"] = ""
                        pass
                    else:
                        item["makeup_id"] = str(value)
                        pass
                    pass
                pass
            items.append(item)
            pass
        pass
        jsonObject["item"] = items
        new_json_str = json.dumps(jsonObject, ensure_ascii=False)
        dialog.close()
        pass

    def reject(self):
        dialog.close()
        pass

    def show(self, json_str=None):
        global ui_dialog
        global dialog
        from submodel.locally.locally_editor import Ui_Dialog
        dialog = QDialog()
        ui_dialog = Ui_Dialog()
        ui_dialog.setupUi(dialog)
        # print("edit locally json:%s" % json_str)
        items = []
        j = json.loads(json_str)
        self.version = j["version"]
        json_array = j["item"]
        table_index = 1
        for item in json_array:
            row_data = [table_index, item["id"], item["name"], item.get("makeup_id")]
            # print(row_data)
            table_index += 1
            items.append(row_data)
            pass
        print(items)
        global table_model
        table_model = LocallyTableModel(data=items)
        ui_dialog.tableView.setModel(table_model)
        ui_dialog.buttonBox.accepted.connect(self.accept)
        ui_dialog.buttonBox.rejected.connect(self.reject)
        dialog.setWindowTitle(FileNames.FILE_LOCALLY_JSON)
        dialog.exec()
        pass


# gogogo 脚本编辑
class GogogoEditor(BaseEditor):
    def show(self, json_str=None):
        pass


# 普通文本编辑
class SimpleEditor(BaseEditor):
    def show(self, json_str=None):
        pass
