import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from .DirectionControlpanel.DirecrtionControlpanel import DirectionControlPanel
from .SppedControl.SpeedControl import SpeedControl
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

        direction_control_panel = DirectionControlPanel()
        speed_control = SpeedControl()
        
        # Create a wrapper widget with title for speed_control
        speed_control_wrapper = QWidget(self)
        speed_control_layout = QVBoxLayout(speed_control_wrapper)
        speed_control_layout.setContentsMargins(0, 0, 0, 0)
        speed_control_title = QLabel("速度控制", speed_control_wrapper)
        speed_control_title_font = QFont()
        speed_control_title_font.setBold(True)
        speed_control_title_font.setPointSize(16)
        speed_control_title.setFont(speed_control_title_font)
        speed_control_title.setStyleSheet("color: rgb(0, 0, 0);")
        speed_control_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        speed_control_title.setFixedHeight(24)
        speed_control_layout.addWidget(speed_control_title)
        speed_control_layout.addWidget(speed_control)
        
        controlwidget = QWidget(self)
        controlwidget.setFixedSize(QSize(1177, 300))
        controlwidgetlayout = QHBoxLayout(controlwidget)
        controlwidgetlayout.setSpacing(0)
        controlwidgetlayout.setContentsMargins(0, 0, 0, 0)
        controlwidgetlayout.addWidget(direction_control_panel, 0)
        controlwidgetlayout.addWidget(speed_control_wrapper, 0)
        controlwidgetlayout.setSpacing(30)
        controlwidgetlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(deviceHint)
        layout.addWidget(controlwidget)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        MainContainer.setLayout(layout)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(MainContainer)

