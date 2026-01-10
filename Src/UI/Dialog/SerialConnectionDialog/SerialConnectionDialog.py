from PyQt6.QtWidgets import QDialog

class SeireConnectionDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(800, 600)