from PyQt5.QtWidgets import QMessageBox


def info(title, msg):
    QMessageBox.information(None, title, msg, QMessageBox.Yes)


def warn(title, msg):
    QMessageBox.warning(None, title, msg, QMessageBox.Yes)
    pass
