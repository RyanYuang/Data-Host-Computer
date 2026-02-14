from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPalette, QColor

from Src.MVP.base_view import BaseView
from .Head.HeadView import HeadView
from .DataMonitor.DataMonitorView import DataMonitorView
from .ControlPanel.ControlPanelView import ControlPanelView
from .SerialConsole.SerialConsoleView import SerialConsoleView


class MainPageView(BaseView):
    """
    MainPage 视图层 - 纯 UI 布局
    不包含任何业务逻辑，所有子 MVP 的组装由 MainPagePresenter 负责
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # 子视图引用（由 Presenter 通过 getter 访问）
        self._head_view: HeadView = None
        self._data_monitor_view: DataMonitorView = None
        self._control_panel_view: ControlPanelView = None
        self._serial_console_view: SerialConsoleView = None

        self._init_ui()

    # ── 子视图 Getter ──
    @property
    def head_view(self) -> HeadView:
        return self._head_view

    @property
    def data_monitor_view(self) -> DataMonitorView:
        return self._data_monitor_view

    @property
    def control_panel_view(self) -> ControlPanelView:
        return self._control_panel_view

    @property
    def serial_console_view(self) -> SerialConsoleView:
        return self._serial_console_view

    # ── 侧栏开关 ──
    def toggle_serial_console(self):
        """切换串口控制台侧栏的展开/收起"""
        console = self._serial_console_view
        if console.isVisible():
            console.hide()
        else:
            console.show()

    # ── UI 初始化 ──
    def _init_ui(self):
        """纯 UI 布局初始化 —— 不涉及 Model / Presenter"""
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(190, 219, 255))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # 创建子视图
        self._head_view = HeadView(self)
        self._head_view.setMinimumSize(self.width(), 68)

        self._data_monitor_view = DataMonitorView(self)
        self._data_monitor_view.setMinimumSize(self.width(), 250)

        self._control_panel_view = ControlPanelView(self)
        self._control_panel_view.setMinimumSize(1225, 454)

        # 串口控制台侧栏（默认隐藏）
        self._serial_console_view = SerialConsoleView(self)
        self._serial_console_view.hide()

        # ── 左侧主内容区 ──
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self._head_view)
        left_layout.addWidget(self._data_monitor_view)
        left_layout.addWidget(self._control_panel_view)

        # ── 水平布局：主内容 + 侧栏 ──
        root_layout = QHBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(left_panel, 1)                # 主内容占满剩余空间
        root_layout.addWidget(self._serial_console_view, 0) # 侧栏固定宽度
        self.setLayout(root_layout)