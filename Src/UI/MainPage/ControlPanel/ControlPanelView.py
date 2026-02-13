from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from Src.MVP.base_view import BaseView
from .DirectionControlPanel.DirectionControlPanelView import DirectionControlPanelView
from .SpeedControl.SpeedControlView import SpeedControlView


class ControlPanelView(BaseView):
    """
    控制面板视图层 —— 纯 UI 布局
    不包含业务逻辑，所有子 MVP 的组装由 ControlPanelPresenter 负责
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._device_hint: QLabel = None
        self._direction_panel_view: DirectionControlPanelView = None
        self._speed_control_view: SpeedControlView = None
        self._speed_control_wrapper: QWidget = None

        self._init_ui()

    # ── 子视图 Getter ──
    @property
    def direction_panel_view(self) -> DirectionControlPanelView:
        return self._direction_panel_view

    @property
    def speed_control_view(self) -> SpeedControlView:
        return self._speed_control_view

    # ── UI 状态更新（由 Presenter 调用） ──
    def set_connected(self, connected: bool):
        """根据连接状态更新 UI 显示"""
        if connected:
            if self._device_hint:
                self._device_hint.hide()
            if self._direction_panel_view:
                self._direction_panel_view.setEnabled(True)
            if self._speed_control_wrapper:
                self._speed_control_wrapper.setEnabled(True)
        else:
            if self._device_hint:
                self._device_hint.show()
            if self._direction_panel_view:
                self._direction_panel_view.setEnabled(False)
            if self._speed_control_wrapper:
                self._speed_control_wrapper.setEnabled(False)

    # ── UI 初始化 ──
    def _init_ui(self):
        main_container = QWidget(self)
        main_container.setStyleSheet(
            "background-color:rgb(255, 255, 255);border-radius:16px;"
        )

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("远程控制面板", main_container)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(20)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgb(0, 0, 0);")
        title_label.setFixedHeight(28)

        # 设备未连接提示
        self._device_hint = QLabel("设备未连接，无法进行远程控制", main_container)
        self._device_hint.setStyleSheet("""
            color:rgb(187,77,0);
            background-color:rgb(254,230,133);
            height:46px;
            width:1177px;
            border-radius:10px;
            padding-left:13px;
        """)
        self._device_hint.setFixedHeight(46)

        # 方向控制面板视图
        self._direction_panel_view = DirectionControlPanelView()

        # 速度控制视图（带标题 wrapper）
        self._speed_control_view = SpeedControlView()
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
        speed_control_layout.addWidget(self._speed_control_view)

        # 控制区域容器
        control_widget = QWidget(self)
        control_widget.setFixedSize(QSize(1177, 300))
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(30)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self._direction_panel_view, 0)
        control_layout.addWidget(self._speed_control_wrapper, 0)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(self._device_hint)
        layout.addWidget(control_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_container.setLayout(layout)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(main_container)

        # 初始状态：未连接
        self.set_connected(False)
