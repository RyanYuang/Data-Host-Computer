from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout

from Src.MVP.base_view import BaseView


class HeadView(BaseView):
    """
    头部视图层 —— 纯 UI
    通过信号将用户操作转发给 Presenter
    """
    # ── 信号定义 ──
    connect_btn_clicked = pyqtSignal()
    alarm_btn_clicked = pyqtSignal(bool)   # 参数: isChecked
    setting_btn_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.TitleLabel: QLabel = None
        self.ConnectButton: QPushButton = None
        self.AlarmButton: QPushButton = None
        self.SettingButton: QPushButton = None

        # 样式预设
        self._connect_btn_default_style = """
            Color:rgb(193,0,7);
            background-color: rgb(255,226,226);
            border-radius: 10px;
            width: 125px;
            height: 40px;
        """
        self._connect_btn_connected_style = """
            Color:rgb(193,0,7);
            background-color: rgb(220, 252, 231);
            border-radius: 10px;
            width: 125px;
            height: 40px;
        """

        self._init_ui()

    # ── 由 Presenter 调用的 UI 更新接口 ──
    def update_connection_status(self, connected: bool):
        """更新连接按钮的显示状态"""
        if connected:
            self.ConnectButton.setText("已连接")
            self.ConnectButton.setStyleSheet(self._connect_btn_connected_style)
        else:
            self.ConnectButton.setText("连接")
            self.ConnectButton.setStyleSheet(self._connect_btn_default_style)

    # ── UI 初始化 ──
    def _init_ui(self):
        # 标题
        self.TitleLabel = QLabel(self)
        self.TitleLabel.setText("环境监测控制系统")
        font = QFont()
        font.setBold(True)
        font.setPointSize(30)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setStyleSheet("color: rgb(0, 0, 0);")

        # 连接按钮
        self.ConnectButton = QPushButton("连接", self)
        self.ConnectButton.setStyleSheet(self._connect_btn_default_style)
        self.ConnectButton.clicked.connect(self.connect_btn_clicked.emit)

        # 告警按钮
        self.AlarmButton = QPushButton("正常", self)
        alarm_icon = QIcon()
        alarm_icon.addFile("Resource/AlarmNormal.png", state=QIcon.State.Off)
        alarm_icon.addFile("Resource/AlarmTrigger.png", state=QIcon.State.On)
        self.AlarmButton.setIcon(alarm_icon)
        self.AlarmButton.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                height: 40px;
                width: 92px;
            }
            QPushButton:checked {
                color: rgb(193,0,7);
                background-color: rgb(255, 226, 226);
            }
            QPushButton:!checked {
                color: rgb(74,85,101);
                background-color: rgb(243,244,246);
            }
        """)
        self.AlarmButton.setCheckable(True)
        self.AlarmButton.clicked.connect(
            lambda: self.alarm_btn_clicked.emit(self.AlarmButton.isChecked())
        )

        # 设置按钮
        setting_icon = QIcon("Resource/SettingIcon.png")
        self.SettingButton = QPushButton(self)
        self.SettingButton.setIcon(setting_icon)
        self.SettingButton.setStyleSheet("""
            QPushButton {
                width: 44px;
                height: 44px;
                border-radius: 10px;
                background-color: rgb(255,255,255);
            }
        """)
        self.SettingButton.clicked.connect(self.setting_btn_clicked.emit)

        # 布局
        layout = QHBoxLayout()
        layout.addWidget(self.TitleLabel)
        layout.addStretch()
        layout.addWidget(self.ConnectButton)
        layout.addWidget(self.AlarmButton)
        layout.addWidget(self.SettingButton)
        self.setLayout(layout)