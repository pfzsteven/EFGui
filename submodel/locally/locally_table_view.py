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
        pass

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self.header)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            col = index.column()
            if col == 1 or col == len(self.header) - 1:
                self._data[index.row()][col] = value
                pass
            else:
                self._data[index.row()][col] = str(value).upper()
            return True
        return False

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return

        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole or (
                role == (QtCore.Qt.DisplayRole or QtCore.Qt.EditRole)):

            row_data = self._data[row]
            if column == 0:
                return row_data[0]
            else:
                if row_data[column] is None:
                    return ""
                else:
                    if column == 1 or column == len(self.header) - 1:
                        return str(row_data[column]).upper()
                    pass
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
