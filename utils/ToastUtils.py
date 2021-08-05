from PyQt5.QtWidgets import QMessageBox


def warn(title, msg):
    QMessageBox.warning(None, title, msg, QMessageBox.Yes)
