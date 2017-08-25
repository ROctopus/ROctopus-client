# Enables automated updates of .ui files created by QtCreator.

from PyQt5 import QtCore, QtGui, QtWidgets
from . import aboutdialog, preferencesdialog, mainwindow, qtresources

Ui_MainWindow = mainwindow.Ui_MainWindow

class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = aboutdialog.Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.icon_lab.setPixmap(QtGui.QPixmap(':/icons/icon.png'))
        self.InitUi()
        self.setWindowIcon(QtGui.QIcon(':/icons/icon.png')) # Relative to runtime directory?

    def InitUi(self):
        self.ui.buttonBox.accepted.connect(self.accept)
        self.show()

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = preferencesdialog.Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.InitUi()
        self.setWindowIcon(QtGui.QIcon(':/icons/icon.png')) # Relative to runtime directory?

    def getValues(self):
        return({
            'username' : self.ui.input_username.text(),
            'pw' : self.ui.input_password.text(), # No way!
            'server_ip' : self.ui.ip_entry.text(),
            'port' : self.ui.port_entry.text(),
            'r_path' : self.ui.input_rpath.text(),
            'r_vers' : self.ui.input_rvers.text(),
            'sys_ram' : self.ui.input_ram.value(),
            'sys_cores' : self.ui.input_cpu.value()
        })

    def chooseFile(self):
        path, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select R Executable')
        self.ui.input_rpath.setText(path)

    def InitUi(self):
        self.ui.settings_buttons.accepted.connect(self.accept)
        self.ui.settings_buttons.rejected.connect(self.reject)
        self.ui.button_path.clicked.connect(self.chooseFile)
