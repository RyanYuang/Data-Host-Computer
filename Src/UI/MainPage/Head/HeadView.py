import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class HeadView(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        # 定义组件
        layout = None
        TitleLable = None
        ConnectButton = None
        AlarmButton = None
        SettingButton = None


        self.InitUI()


    def InitUI(self):
        """
        @berif 初始化UI
        :return:
        """
        TitleLable = QLabel(self)
        TitleLable.setText("环境监测控制系统")
        Font = QFont()
        Font.setBold(True)
        Font.setPointSize(30)
        TitleLable.setFont(Font)
        TitleLable.setStyleSheet("""
            Color:rgb(0, 0, 0);
             """)
        # spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        ConnectButton = QPushButton(self)
        ConnectButton.resize(125,40)

        AlarmButton = QPushButton(self)


        layout = QVBoxLayout()
        layout.addWidget(TitleLable)
        # layout.addItem(spacer)
        layout.addWidget(ConnectButton)
