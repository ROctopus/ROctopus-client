from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import ipdb

class roctoTableModel(QtCore.QAbstractTableModel):
    # pandas.sandbox has nice examples to inspire here.
    def __init__(self, rocto_pack):
        super().__init__()
        self.rocto_pack = rocto_pack
        self.__gridReorganize()

    def __gridReorganize(self):
        # Add a column to let user select which settings to run.
        select_col = 'Run?'
        
        # a dict yields its keys when iterated
        pars =  [*self.rocto_pack.grid[0]]

        for i in self.rocto_pack.grid:
            i[select_col] = 2 # = QtCore.Qt.Checked
        
        self.rocto_pack.columns = [select_col] + pars

    @pyqtSlot(QtCore.QModelIndex)
    def _handle_doubleclicked(self, model_index):
        if model_index.column() == 0:
            if self.data(model_index, QtCore.Qt.CheckStateRole) == 2:
                self.setData(model_index, 0, QtCore.Qt.CheckStateRole) # 0 = QtCore.Qt.Unchecked
            else:
                self.setData(model_index, 2, QtCore.Qt.CheckStateRole)

    # Required subclassing definitions: https://doc.qt.io/qt-5/qabstractitemmodel.html#subclassing
    def columnCount(self, model_index):
        return len(self.rocto_pack.columns)

    def rowCount(self, model_index):
        return len(self.rocto_pack.grid)

    def data(self, model_index, role):
        if role == QtCore.Qt.DisplayRole and model_index.column() != 0:
            param = self.rocto_pack.columns[model_index.column()]
            return self.rocto_pack.grid[model_index.row()][param]
        elif role == QtCore.Qt.CheckStateRole and model_index.column() == 0:
            param = self.rocto_pack.columns[model_index.column()]
            return self.rocto_pack.grid[model_index.row()][param]
        elif role == QtCore.Qt.DisplayRole and model_index.column() == 0:
            return QtCore.QVariant

    def flags(self, model_index):
        if model_index.column() == 0:
            return QtCore.Qt.ItemIsUserCheckable and QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.rocto_pack.columns[section]
        else:
            return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    def setData(self, model_index, value, role):
        if role == QtCore.Qt.CheckStateRole and model_index.column() == 0:
            param = self.rocto_pack.columns[model_index.column()]
            self.rocto_pack.grid[model_index.row()][param] = value
        self.dataChanged.emit(model_index, model_index)
