from PyQt5 import QtCore


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

        # [[1, 'F24', '原图', None], [2, 'F20', '鲜明', 'MK11'], [3, 'F23', '暗调', 'MK11'], [4, 'F07', '金属', 'MK07'],
        #  [5, 'F26', '尼龙', 'MK14'], [6, 'F31', '海街', 'MK01'], [7, 'F10', '昭和', 'MK09'], [8, 'F30', '美国派', 'MK13'],
        #  [9, 'F33', '春夏', 'MK05']]
        if role == QtCore.Qt.DisplayRole:
            row_data = self._data[row]


    # if row < len(self._data):
    #     columns = self._data[row]
    #     print(columns)

    # if role == QtCore.Qt.DisplayRole:
    #     if column == 0:
    #         return self._data[row].id
    #     else:
    #         box = QtWidgets.QLineEdit()
    #         box.setText('X')
    #
    #         return [box]
    #     pass
    # pass

    pass
