from abc import ABCMeta, abstractmethod


class BaseEditor(metaclass=ABCMeta):

    def __init__(self):
        self.file_path = None
        self.callback = None

    @abstractmethod
    def show(self, file_path, text=None, callback=None):
        pass
