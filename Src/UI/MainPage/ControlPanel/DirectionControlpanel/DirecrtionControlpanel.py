import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, \
    QGridLayout


class DirectionControlPanel(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setMinimumSize(QSize(256, 300))
        self.initUI()
        self.setStyleSheet("""
            QPushButton{
                background-color:rgb(255, 255, 255);
                border-radius:10px;
                height:46px;
                width:46px;
            }
            background-color:rgb(0, 0, 255);
        """)
    def initUI(self):
        MainContainer = QWidget(self)
        MainContainer.setMinimumSize(QSize(256, 300))
        MainContainer.setStyleSheet("""
            QPushButton{
                color:rgb(106, 114, 130);
                background-color:rgb(209, 213, 220);
            }
        """)
        layout = QGridLayout()
        LeftBtn = QPushButton("Left")
        LeftBtn.setMinimumSize(QSize(80, 64))
        LeftBtn.setStyleSheet("""
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
        """)
        RightBtn = QPushButton("Right")
        RightBtn.setMinimumSize(QSize(80, 64))
        RightBtn.setStyleSheet("""
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        UpBtn = QPushButton("Up")
        UpBtn.setMinimumSize(QSize(64, 80))
        UpBtn.setStyleSheet("""
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        DownBtn = QPushButton("Down")
        DownBtn.setMinimumSize(QSize(20, 80))
        DownBtn.setStyleSheet("""
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        MidBtn = QPushButton("Stop")
        MidBtn.setMinimumSize(QSize(80, 80))
        MidBtn.setStyleSheet("""
            border-radius: 40px
        """)
        layout.addWidget(UpBtn, 0, 1)
        layout.addWidget(LeftBtn, 1, 0)
        layout.addWidget(MidBtn, 1, 1)
        layout.addWidget(RightBtn, 1, 2)
        layout.addWidget(DownBtn, 2, 1)
        MainContainer.setLayout(layout)
        parent_layout = QVBoxLayout(self)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(MainContainer)
