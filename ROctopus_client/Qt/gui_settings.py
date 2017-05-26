# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.ip_label = QtWidgets.QLabel(self.groupBox)
        self.ip_label.setObjectName("ip_label")
        self.gridLayout.addWidget(self.ip_label, 0, 0, 1, 1)
        self.ip_entry = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip_entry.sizePolicy().hasHeightForWidth())
        self.ip_entry.setSizePolicy(sizePolicy)
        self.ip_entry.setMinimumSize(QtCore.QSize(15, 0))
        self.ip_entry.setObjectName("ip_entry")
        self.gridLayout.addWidget(self.ip_entry, 0, 1, 1, 2)
        self.port_label = QtWidgets.QLabel(self.groupBox)
        self.port_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.port_label.setObjectName("port_label")
        self.gridLayout.addWidget(self.port_label, 1, 0, 1, 1)
        self.port_entry = QtWidgets.QLineEdit(self.groupBox)
        self.port_entry.setMaximumSize(QtCore.QSize(45, 16777215))
        self.port_entry.setObjectName("port_entry")
        self.gridLayout.addWidget(self.port_entry, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 29, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.groupBox.setTitle(_translate("Dialog", "Server Settings"))
        self.ip_label.setText(_translate("Dialog", "Server IP:"))
        self.port_label.setText(_translate("Dialog", "Port"))

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.InitUi()

        self.ui.ip_entry.setInputMask('000.000.000.000')
        self.ui.port_entry.setInputMask('00000')
    def getValues(self):
        return({
            'server_ip' : self.ui.ip_entry.text(),
            'port' : self.ui.port_entry.text()
        })

    def InitUi(self):
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        # self.show()
