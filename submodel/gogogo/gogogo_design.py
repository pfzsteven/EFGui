# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gogogo_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(486, 640)
        Form.setAutoFillBackground(True)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(0, 50, 491, 241))
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 489, 239))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.et_script = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.et_script.setGeometry(QtCore.QRect(10, 0, 461, 241))
        self.et_script.setAutoFillBackground(True)
        self.et_script.setAcceptRichText(False)
        self.et_script.setObjectName("et_script")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 300, 121, 21))
        self.label.setObjectName("label")
        self.cb_iphone6 = QtWidgets.QCheckBox(Form)
        self.cb_iphone6.setGeometry(QtCore.QRect(10, 340, 87, 20))
        self.cb_iphone6.setObjectName("cb_iphone6")
        self.cb_iphone8 = QtWidgets.QCheckBox(Form)
        self.cb_iphone8.setGeometry(QtCore.QRect(120, 340, 87, 20))
        self.cb_iphone8.setObjectName("cb_iphone8")
        self.cb_iphonex = QtWidgets.QCheckBox(Form)
        self.cb_iphonex.setGeometry(QtCore.QRect(220, 340, 87, 20))
        self.cb_iphonex.setObjectName("cb_iphonex")
        self.cb_iphone12 = QtWidgets.QCheckBox(Form)
        self.cb_iphone12.setGeometry(QtCore.QRect(10, 380, 87, 20))
        self.cb_iphone12.setObjectName("cb_iphone12")
        self.cb_only_front = QtWidgets.QCheckBox(Form)
        self.cb_only_front.setGeometry(QtCore.QRect(120, 440, 87, 20))
        self.cb_only_front.setObjectName("cb_only_front")
        self.cb_only_back = QtWidgets.QCheckBox(Form)
        self.cb_only_back.setGeometry(QtCore.QRect(230, 440, 87, 20))
        self.cb_only_back.setObjectName("cb_only_back")
        self.cb_gen_all = QtWidgets.QCheckBox(Form)
        self.cb_gen_all.setGeometry(QtCore.QRect(10, 440, 87, 20))
        self.cb_gen_all.setChecked(True)
        self.cb_gen_all.setObjectName("cb_gen_all")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 410, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.btn_save = QtWidgets.QPushButton(Form)
        self.btn_save.setGeometry(QtCore.QRect(340, 10, 113, 32))
        self.btn_save.setObjectName("btn_save")
        self.cb_iphone11 = QtWidgets.QCheckBox(Form)
        self.cb_iphone11.setGeometry(QtCore.QRect(320, 340, 87, 20))
        self.cb_iphone11.setObjectName("cb_iphone11")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "gogogo????????????"))
        self.label.setText(_translate("Form", "??????????????????"))
        self.cb_iphone6.setText(_translate("Form", "iPhone6"))
        self.cb_iphone8.setText(_translate("Form", "iPhone8"))
        self.cb_iphonex.setText(_translate("Form", "iPhoneX"))
        self.cb_iphone12.setText(_translate("Form", "iPhone12"))
        self.cb_only_front.setText(_translate("Form", "???????????????"))
        self.cb_only_back.setText(_translate("Form", "???????????????"))
        self.cb_gen_all.setText(_translate("Form", "???????????????"))
        self.btn_save.setText(_translate("Form", "??????"))
        self.cb_iphone11.setText(_translate("Form", "iPhone11"))
