# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(402, 365)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.get_task = QtWidgets.QWidget()
        self.get_task.setObjectName("get_task")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.get_task)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 6, 1, 1)
        self.avaliable_tasks = QtWidgets.QLabel(self.get_task)
        self.avaliable_tasks.setEnabled(False)
        self.avaliable_tasks.setObjectName("avaliable_tasks")
        self.gridLayout_2.addWidget(self.avaliable_tasks, 0, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.get_task)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 3, 1, 1)
        self.connect_button = QtWidgets.QPushButton(self.get_task)
        self.connect_button.setEnabled(True)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout_2.addWidget(self.connect_button, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.get_task)
        self.start_button.setEnabled(False)
        self.start_button.setObjectName("start_button")
        self.gridLayout_2.addWidget(self.start_button, 1, 0, 1, 1)
        self.runBox = QtWidgets.QGroupBox(self.get_task)
        self.runBox.setEnabled(False)
        self.runBox.setAccessibleName("")
        self.runBox.setAutoFillBackground(False)
        self.runBox.setFlat(False)
        self.runBox.setCheckable(False)
        self.runBox.setObjectName("runBox")
        self.gridLayout = QtWidgets.QGridLayout(self.runBox)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.runBox)
        self.textEdit.setEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.runBox, 2, 0, 1, 7)
        self.tabWidget.addTab(self.get_task, "")
        self.submit_task = QtWidgets.QWidget()
        self.submit_task.setObjectName("submit_task")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.submit_task)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableView = QtWidgets.QTableView(self.submit_task)
        self.tableView.setEnabled(False)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setWordWrap(False)
        self.tableView.setObjectName("tableView")
        self.gridLayout_4.addWidget(self.tableView, 2, 0, 1, 5)
        self.label_3 = QtWidgets.QLabel(self.submit_task)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.submit_task)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.lab_sel_file_name = QtWidgets.QLabel(self.submit_task)
        self.lab_sel_file_name.setText("")
        self.lab_sel_file_name.setObjectName("lab_sel_file_name")
        self.gridLayout_4.addWidget(self.lab_sel_file_name, 0, 1, 1, 1)
        self.select_rocto = QtWidgets.QPushButton(self.submit_task)
        self.select_rocto.setObjectName("select_rocto")
        self.gridLayout_4.addWidget(self.select_rocto, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 3, 1, 1)
        self.submit_button = QtWidgets.QPushButton(self.submit_task)
        self.submit_button.setEnabled(False)
        self.submit_button.setIconSize(QtCore.QSize(16, 16))
        self.submit_button.setObjectName("submit_button")
        self.gridLayout_4.addWidget(self.submit_button, 3, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 3, 0, 1, 3)
        self.tabWidget.addTab(self.submit_task, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 402, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(True)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setEnabled(True)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionLicense_Information = QtWidgets.QAction(MainWindow)
        self.actionLicense_Information.setObjectName("actionLicense_Information")
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionLicense_Information)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rocto Client"))
        self.avaliable_tasks.setText(_translate("MainWindow", "N/A"))
        self.label.setText(_translate("MainWindow", "Available tasks:"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))
        self.start_button.setText(_translate("MainWindow", "Start worker!"))
        self.runBox.setTitle(_translate("MainWindow", "Logs:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.get_task), _translate("MainWindow", "Get"))
        self.label_3.setText(_translate("MainWindow", "Selected file:"))
        self.label_2.setText(_translate("MainWindow", "Job details:"))
        self.select_rocto.setText(_translate("MainWindow", "Select"))
        self.submit_button.setText(_translate("MainWindow", "Submit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.submit_task), _translate("MainWindow", "Submit"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuEdit.setTitle(_translate("MainWindow", "&Edit"))
        self.menuAbout.setTitle(_translate("MainWindow", "&About"))
        self.actionPreferences.setText(_translate("MainWindow", "&Preferences"))
        self.actionPreferences.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About ROctopus"))
        self.actionLicense_Information.setText(_translate("MainWindow", "License Information"))

