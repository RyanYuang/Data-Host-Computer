from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout


class SeireConnectionDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(672, 320)
        layout  = QVBoxLayout()

        # Head
        titleWidget = QWidget(self)
        titleWidget.setLayout(QHBoxLayout())

        icon_label = QLabel(self)
        pixmap = QPixmap("Resource/Connection Dialog Iocn.png")
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel(self)
        title.setText("串口连接配置")
        titleWidget.layout().addWidget(icon_label)
        titleWidget.layout().addWidget(title)
        # 串口选择
        layout.addWidget(titleWidget)
        self.setLayout(layout)