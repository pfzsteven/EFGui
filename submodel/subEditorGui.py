import json
from abc import ABCMeta, abstractmethod

from PyQt5.QtWidgets import QDialog

from submodel.table_view import LocallyTableModel


class BaseEditor(metaclass=ABCMeta):

    @abstractmethod
    def show(self, json_str=None):
        pass


# locally.json 编辑
class LocallyFileEditor(BaseEditor):

    def show(self, json_str=None):
        global ui_dialog
        from submodel.locally_editor import Ui_Dialog
        qDialog = QDialog()
        ui_dialog = Ui_Dialog()
        ui_dialog.setupUi(qDialog)
        # print("edit locally json:%s" % json_str)
        items = []
        j = json.loads(json_str)
        json_array = j["item"]
        table_index = 1
        for item in json_array:
            row_data = [table_index, item["id"], item["name"], item.get("makeup_id")]
            # print(row_data)
            table_index += 1
            items.append(row_data)
            pass
        print(items)
        model = LocallyTableModel(data=items)
        ui_dialog.tableView.setModel(model)
        qDialog.exec()
        pass


# gogogo 脚本编辑
class GogogoEditor(BaseEditor):
    def show(self, json_str=None):
        pass
