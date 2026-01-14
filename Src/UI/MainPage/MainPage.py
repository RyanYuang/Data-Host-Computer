from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from .Head.HeadView import HeadView
from .DataMonitor.DataMonitor import DataItem, DataMonitor
from .ControlPanel.ControlPanel import ControlPanel
class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(190, 219, 255))  # 设置浅蓝色背景
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 启用自动填充背景

        # 初始化组件
        head_view = HeadView()  # 创建 HeadView 的实例
        head_view.setMinimumSize(self.width(), 68)
        data_monitor = DataMonitor()  # 创建 DataMonitor 实例
        data_monitor.setMinimumSize(self.width(), 250)
        control_panel = ControlPanel()
        control_panel.setMinimumSize(1225,454)

        # 初始化layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(head_view)  # 将 HeadView 实例添加到布局中
        layout.addWidget(data_monitor)  # 将 DataMonitor 实例添加到布局中
        layout.addWidget(control_panel)
        self.setLayout(layout)