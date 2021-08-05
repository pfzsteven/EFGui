# gogogo 脚本编辑
from PyQt5.QtWidgets import QDialog

from submodel.gogogo.gogogo import Ui_Form
from submodel.interfaces import BaseEditor
from utils import FileUtils


class GogogoEditor(BaseEditor):

    def __init__(self):
        super().__init__()
        self.text = ""
        pass

    def save(self):
        gen_all = form.cb_gen_all
        gen_only_front = form.cb_only_front
        gen_only_back = form.cb_only_back
        text = form.et_script.toPlainText()
        FileUtils.writeString2File(path=self.file_path, text=text)
        self.callback(self.file_path, text,
                      (gen_all.isChecked(), gen_only_front.isChecked(), gen_only_back.isChecked()),
                      (form.cb_iphone6.isChecked(),
                       form.cb_iphone8.isChecked(),
                       form.cb_iphonex.isChecked(),
                       form.cb_iphone11.isChecked(),
                       form.cb_iphone12.isChecked()))
        dialog.close()
        pass

    def init(self):
        form.et_script.setPlainText(self.text)
        form.btn_save.clicked.connect(self.save)
        pass

    def show(self, file_path, text=None, callback=None):
        self.file_path = file_path
        self.callback = callback
        self.text = text
        global form
        global dialog
        dialog = QDialog()
        form = Ui_Form()
        form.setupUi(dialog)
        self.init()
        dialog.exec()
        pass
