# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/aboutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(323, 154)
        self.gridLayout = QtWidgets.QGridLayout(AboutDialog)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_lab = QtWidgets.QLabel(AboutDialog)
        self.icon_lab.setMaximumSize(QtCore.QSize(100, 100))
        self.icon_lab.setText("")
        self.icon_lab.setPixmap(QtGui.QPixmap("icons/icon.png"))
        self.icon_lab.setScaledContents(True)
        self.icon_lab.setIndent(-1)
        self.icon_lab.setObjectName("icon_lab")
        self.horizontalLayout.addWidget(self.icon_lab)
        self.about_text = QtWidgets.QLabel(AboutDialog)
        self.about_text.setObjectName("about_text")
        self.horizontalLayout.addWidget(self.about_text)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "AboutDialog"))
        self.about_text.setText(_translate("AboutDialog", "<html><head/><body><p>ROctopus Client</p><p>Erik-Jan van Kesteren (<a href=\"https://github.com/vankesteren\"><span style=\" text-decoration: underline; color:#0000ff;\">GitHub</span></a>)<br/>Oğuzhan Öğreden (<a href=\"https://github.com/oguzhanogreden\"><span style=\" text-decoration: underline; color:#0000ff;\">GitHub</span></a>)</p></body></html>"))
