import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import client

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(329, 220)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.get_task = QtWidgets.QPushButton(self.centralWidget)
        self.get_task.setGeometry(QtCore.QRect(80, 62, 80, 25))
        self.get_task.setObjectName("get_task")
        self.quit_button = QtWidgets.QPushButton(self.centralWidget)
        self.quit_button.setGeometry(QtCore.QRect(230, 140, 80, 30))
        self.quit_button.setObjectName("quit_button")
        self.ip_entry = QtWidgets.QLineEdit(self.centralWidget)
        self.ip_entry.setGeometry(QtCore.QRect(90, 21, 125, 25))
        self.ip_entry.setObjectName("ip_entry")
        self.ip_label = QtWidgets.QLabel(self.centralWidget)
        self.ip_label.setGeometry(QtCore.QRect(20, 24, 71, 16))
        self.ip_label.setObjectName("ip_label")
        self.port_entry = QtWidgets.QLineEdit(self.centralWidget)
        self.port_entry.setGeometry(QtCore.QRect(260, 21, 48, 25))
        self.port_entry.setObjectName("port_entry")
        self.start_task = QtWidgets.QPushButton(self.centralWidget)
        self.start_task.setGeometry(QtCore.QRect(170, 62, 80, 25))
        self.start_task.setObjectName("start_task")
        self.port_label = QtWidgets.QLabel(self.centralWidget)
        self.port_label.setGeometry(QtCore.QRect(223, 21, 31, 20))
        self.port_label.setObjectName("port_label")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(21, 111, 111, 21))
        self.label.setObjectName("label")
        self.task_info = QtWidgets.QLabel(self.centralWidget)
        self.task_info.setGeometry(QtCore.QRect(140, 111, 131, 21))
        self.task_info.setObjectName("task_info")
        self.get_task.raise_()
        self.quit_button.raise_()
        self.ip_entry.raise_()
        self.ip_label.raise_()
        self.port_entry.raise_()
        self.port_label.raise_()
        self.start_task.raise_()
        self.label.raise_()
        self.task_info.raise_()
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        MainWindow.insertToolBarBreak(self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionLicense_Informatipn = QtWidgets.QAction(MainWindow)
        self.actionLicense_Informatipn.setObjectName("actionLicense_Informatipn")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setWindowIcon(QtGui.QIcon('icons/icon.png'))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ROctopus Worker"))
        self.get_task.setText(_translate("MainWindow", "Get Task"))
        self.quit_button.setText(_translate("MainWindow", "Quit"))
        self.ip_label.setText(_translate("MainWindow", "Server IP:"))
        self.start_task.setText(_translate("MainWindow", "Start Task"))
        self.port_label.setText(_translate("MainWindow", "Port"))
        self.label.setText(_translate("MainWindow", "Current Task ID:"))
        self.task_info.setText(_translate("MainWindow", "-"))
        self.actionLicense_Informatipn.setText(_translate("MainWindow", "License Informatipn"))



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.InitUi()

    def InitUi(self):
        self.ui.quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.get_task.clicked.connect(self.get_task)
        self.ui.start_task.clicked.connect(self.start_task)
        self.show()

    def get_task(self):
        self.statusBar().showMessage('Getting task from: ' + self.ui.ip_entry.text() + ':' + self.ui.port_entry.text())
        self.task = client.Task(self.ui.ip_entry.text(), self.ui.port_entry.text())
        self.ui.task_info.setText(str(self.task.id))
        self.statusBar().showMessage('Task arrived!')

    def start_task(self):
        self.statusBar().showMessage('Task starts! Window will hang :(')
        self.task.run()
        self.statusBar().showMessage('Task finished!')
        self.task.send_results(self.ui.ip_entry.text(), self.ui.port_entry.text())
        self.statusBar().showMessage('Task output sent back!')
