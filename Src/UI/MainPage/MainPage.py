from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

from Src.MVP.base_view import BaseView
from .Head.HeadView import HeadView
from .DataMonitor.DataMonitorView import DataMonitorView
from .ControlPanel.ControlPanelView import ControlPanelView


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

        # 布局
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._head_view)
        layout.addWidget(self._data_monitor_view)
        layout.addWidget(self._control_panel_view)
        self.setLayout(layout)