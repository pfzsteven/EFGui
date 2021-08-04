from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt


class LocallyTableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.header = ['序号', '滤镜ID(*)', '滤镜名(*)', '妆容ID']
        pass

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return

        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole:
            row_data = self._data[row]
            if column == 0:
                return row_data[0]
            else:
                if row_data[column] is None:
                    return ""
                else:
                    return str(row_data[column])
                pass
            pass
        pass

    def flags(self, index: QModelIndex):
        column = index.column()
        if column == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
