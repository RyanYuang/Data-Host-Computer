from PyQt6.QtWidgets import QWidget

class BaseView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._presenter = None

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter = presenter