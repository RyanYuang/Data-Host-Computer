import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, \
    QGridLayout, QButtonGroup


class SpeedParament:
    def __init__(self,percentage = 0):
        super(SpeedParament, self).__init__()
        self.percentage = percentage

class SpeedControl(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.SpeedParamentlist = []
        self.SpeedParamentlist.append(SpeedParament(25))
        self.SpeedParamentlist.append(SpeedParament(50))
        self.SpeedParamentlist.append(SpeedParament(75))
        self.SpeedParamentlist.append(SpeedParament(100))
        self.initUI()
    def initUI(self):
        Maincontainer = QWidget(self)
        Maincontainer.setMinimumSize(QSize(200, 300))
        layout = QHBoxLayout()
        title = QLabel(self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setText("Speed Control")
        buttons = []
        buttonsgroup = QButtonGroup(self)
        for i in range(0,4):
            buttons.append(QPushButton(str(self.SpeedParamentlist[i].percentage)+'%'))
            buttonsgroup.addButton(buttons[i])
            buttons[i].setCheckable(True)
            buttons[i].setStyleSheet("""
                QPushButton {
                    border-radius: 10px;
                    background-color: rgb(243, 244, 246);
                    color: rgb(0, 0, 0);
                    }
                    QPushButton:checked 
                    {
                        background-color: rgb(21, 93, 252);
                        color:rgb(255, 255, 255);
                    }
                """)
            buttons[i].setMinimumSize(QSize(137, 36))
            layout.addWidget(buttons[i])
        Maincontainer.setLayout(layout)
        parent_layout = QVBoxLayout(self)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(title)
        parent_layout.addWidget(Maincontainer)

