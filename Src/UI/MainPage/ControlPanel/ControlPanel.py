import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout


class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        
        # 初始化UI
        self.initUI()
        
    def initUI(self):

        MainContainer = QWidget(self)
        MainContainer.setStyleSheet("background-color:rgb(255, 255, 255);border-radius:16px;")
        """初始化控制面板UI"""
        layout = QVBoxLayout()
        title_label = QLabel("远程控制面板", MainContainer)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(20)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgb(0, 0, 0);")
        title_label.setFixedHeight(28)

        deviceHint = QLabel("设备未连接，无法进行远程控制",MainContainer)
        deviceHintfont = QFont()
        deviceHintfont.setPointSize(14)
        deviceHint.setFont(QFont())
        deviceHint.setStyleSheet("""
            color:rgb(187,77,0);
            background-color:rgb(254,230,133);
            height:46px;
            width:1177px;
            border-radius:10px;
            padding-left:13px;
        """)
        deviceHint.setFixedHeight(46)

        # controlwidget = QWidget(self)
        # controlwidget.setLayout(QHBoxLayout())




        layout.addWidget(title_label)
        layout.addWidget(deviceHint)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        MainContainer.setLayout(layout)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(MainContainer)

        
        # # 设置布局
        # layout = QVBoxLayout()
        #
        # # 添加标题
        # title_label = QLabel("控制面板", self)
        # title_font = QFont()
        # title_font.setBold(True)
        # title_font.setPointSize(18)
        # title_label.setFont(title_font)
        # title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # title_label.setStyleSheet("color: rgb(50, 50, 50); margin: 10px;")
        # layout.addWidget(title_label)
        #
        # # 添加一些控制按钮作为示例
        # button_layout = QHBoxLayout()
        #
        # start_button = QPushButton("启动", self)
        # start_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: rgb(76, 175, 80);
        #         color: white;
        #         border-radius: 8px;
        #         padding: 8px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: rgb(60, 140, 65);
        #     }
        # """)
        #
        # stop_button = QPushButton("停止", self)
        # stop_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: rgb(244, 67, 54);
        #         color: white;
        #         border-radius: 8px;
        #         padding: 8px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: rgb(200, 50, 40);
        #     }
        # """)
        #
        # reset_button = QPushButton("重置", self)
        # reset_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: rgb(33, 150, 243);
        #         color: white;
        #         border-radius: 8px;
        #         padding: 8px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: rgb(25, 120, 200);
        #     }
        # """)
        #
        # button_layout.addWidget(start_button)
        # button_layout.addWidget(stop_button)
        # button_layout.addWidget(reset_button)
        # button_layout.addStretch()  # 添加弹性空间
        #
        # layout.addLayout(button_layout)
        #
        # # 添加弹性空间
        # layout.addStretch()
        #
        # # 设置布局
        # self.setLayout(layout)