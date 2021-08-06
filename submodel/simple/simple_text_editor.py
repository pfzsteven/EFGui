# 普通文本编辑
from PyQt5.QtWidgets import QDialog

from submodel.interfaces import BaseEditor
from submodel.simple.simple_design import Ui_Dialog
from utils import FileUtils


class SimpleEditor(BaseEditor):

    def __init__(self):
        super().__init__()
        self.text = ""
        pass

    def save(self):
        new_text = ui_dialog.et_script.toPlainText()
        FileUtils.writeString2File(path=self.file_path, text=new_text)
        self.callback(self.file_path, new_text)
        dialog.close()
        pass

    def initWidget(self):
        ui_dialog.btn_save.clicked.connect(self.save)
        ui_dialog.et_script.setPlainText(self.text)
        pass

    def show(self, file_path, text=None, callback=None):
        self.file_path = file_path
        self.callback = callback
        self.text = text
        global ui_dialog
        global dialog
        ui_dialog = Ui_Dialog()
        dialog = QDialog()
        ui_dialog.setupUi(dialog)
        self.initWidget()
        dialog.exec()
        pass
