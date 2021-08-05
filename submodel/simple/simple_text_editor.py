# 普通文本编辑
from submodel.interfaces import BaseEditor


class SimpleEditor(BaseEditor):

    def __init__(self):
        super().__init__()
        pass

    def show(self, file_path, text=None, callback=None):
        self.file_path = file_path
        self.callback = callback
        pass
