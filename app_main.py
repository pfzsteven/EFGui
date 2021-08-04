import sys

from PyQt5 import QtWidgets

from main_editor import Ui_Dialog

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    dialog = Ui_Dialog()
    dialog.setupUi(form)
    form.show()
    sys.exit(app.exec_())
