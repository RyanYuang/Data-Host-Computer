import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from .DirectionControlPanel.DirectionControlPanelView import DirectionControlPanelView
from .DirectionControlPanel.DirectionControlPanelModel import DirectionControlPanelModel
from .DirectionControlPanel.DirectionControlPanelPresenter import DirectionControlPanelPresenter
from .SppedControl.SpeedControl import SpeedControl
from Src.Serial.SerialManager import SerialManager
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager

# 使用 QObject 避免元类冲突，同时可以处理消息
class ControlPanel(QWidget):
    """控制面板 - 监听连接状态"""
    
    def __init__(self, parent=None, message_manager: MessageManager = None):
        super(QWidget, self).__init__(parent)
        
        self.serial_manager = SerialManager()
        self._message_manager = message_manager
        self._deviceHint = None
        self._direction_panel = None
        self._speed_control_wrapper = None
        
        # 保存控件引用供更新使用
        self._widgets = {}
        
        self.initUI()

    def set_message_manager(self, message_manager: MessageManager):
        """设置消息管理器"""
        self._message_manager = message_manager
        
    def initUI(self):
        MainContainer = QWidget(self)
        MainContainer.setStyleSheet("background-color:rgb(255, 255, 255);border-radius:16px;")
        
        layout = QVBoxLayout()
        title_label = QLabel("远程控制面板", MainContainer)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(20)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgb(0, 0, 0);")
        title_label.setFixedHeight(28)

        # 设备未连接提示
        self._deviceHint = QLabel("设备未连接，无法进行远程控制", MainContainer)
        self._deviceHint.setFont(QFont())
        self._deviceHint.setStyleSheet("""
            color:rgb(187,77,0);
            background-color:rgb(254,230,133);
            height:46px;
            width:1177px;
            border-radius:10px;
            padding-left:13px;
        """)
        self._deviceHint.setFixedHeight(46)

        direction_control_panel_view = DirectionControlPanelView()
        direction_control_panel_model = DirectionControlPanelModel()
        direction_control_panel_presenter = DirectionControlPanelPresenter(
            view=direction_control_panel_view,
            model=direction_control_panel_model
        )
        self._direction_panel = direction_control_panel_view
        speed_control = SpeedControl()

        # Create a wrapper widget with title for speed_control
        self._speed_control_wrapper = QWidget(self)
        speed_control_layout = QVBoxLayout(self._speed_control_wrapper)
        speed_control_layout.setContentsMargins(0, 0, 0, 0)
        speed_control_title = QLabel("速度控制", self._speed_control_wrapper)
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
        controlwidgetlayout.addWidget(direction_control_panel_view, 0)
        controlwidgetlayout.addWidget(self._speed_control_wrapper, 0)
        controlwidgetlayout.setSpacing(30)
        controlwidgetlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(self._deviceHint)
        layout.addWidget(controlwidget)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        MainContainer.setLayout(layout)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(MainContainer)
        
        # 初始更新UI状态
        self._update_connection_ui()

    def _update_connection_ui(self):
        """根据连接状态更新UI"""
        connected = self.serial_manager.GetSerialStatus()
        print(f"[ControlPanel] 连接状态: {connected}")
        
        if connected:
            # 已连接：隐藏提示，启用控制面板
            if self._deviceHint:
                self._deviceHint.hide()
            if self._direction_panel:
                self._direction_panel.setEnabled(True)
            if self._speed_control_wrapper:
                self._speed_control_wrapper.setEnabled(True)
        else:
            # 未连接：显示提示，禁用控制面板
            if self._deviceHint:
                self._deviceHint.show()
            if self._direction_panel:
                self._direction_panel.setEnabled(False)
            if self._speed_control_wrapper:
                self._speed_control_wrapper.setEnabled(False)

    def on_serial_status_changed(self, connected: bool):
        """外部调用的回调方法 - 更新连接状态UI"""
        self._update_connection_ui()

