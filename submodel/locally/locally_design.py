# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'locally_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(471, 640)
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 70, 451, 561))
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableView.setGridStyle(QtCore.Qt.DashDotLine)
        self.tableView.setSortingEnabled(False)
        self.tableView.setObjectName("tableView")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 20, 181, 32))
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.btn_delete_row = QtWidgets.QPushButton(Dialog)
        self.btn_delete_row.setGeometry(QtCore.QRect(290, 20, 113, 32))
        self.btn_delete_row.setObjectName("btn_delete_row")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_delete_row.setText(_translate("Dialog", "删除选中行"))
