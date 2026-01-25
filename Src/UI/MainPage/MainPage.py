from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

from .Head.HeadView import HeadView
from .Head.HeadModel import HeadModel
from .Head.HeadPresenter import HeadPresenter
from Src.Message.MessageManager import MessageManager
from .DataMonitor.DataMonitorView import DataMonitorView
from .DataMonitor.DataMonitorModel import DataMonitorModel
from .DataMonitor.DataMonitorPresenter import DataMonitorPresenter
from .ControlPanel.ControlPanel import ControlPanel
from Src.MVP import BasePresenter

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self._message_manager = MessageManager() # Create a single message manager instance

        self.initUI()
    def set_presenter(self,Presenter: BasePresenter):
        self.Presenter = Presenter
    def initUI(self):
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(190, 219, 255))  # 设置浅蓝色背景
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 启用自动填充背景

        # 初始化组件 for Head
        head_model = HeadModel()
        head_view = HeadView(self)
        self._head_presenter = HeadPresenter(view=head_view, model=head_model, message_manager=self._message_manager)
        head_view.setMinimumSize(self.width(), 68)

        # --- DataMonitor MVP Setup ---
        data_monitor_view = DataMonitorView()
        data_monitor_model = DataMonitorModel()
        self._data_monitor_presenter = DataMonitorPresenter(data_monitor_view, data_monitor_model, self._message_manager)
        data_monitor_view.setMinimumSize(self.width(), 250)
        
        control_panel = ControlPanel()
        control_panel.setMinimumSize(1225,454)

        # 初始化layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(head_view)  # 将 HeadView 实例添加到布局中
        layout.addWidget(data_monitor_view)  # 将 DataMonitorView 实例添加到布局中
        layout.addWidget(control_panel)
        self.setLayout(layout)