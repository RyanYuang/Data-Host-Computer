from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from .Head.HeadView import HeadView

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置背景颜色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(190, 219, 255))  # 设置浅灰色背景
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 启用自动填充背景

        # 初始化组件
        head_view = HeadView()  # 创建 HeadView 的实例
        head_view.resize(self.width(), 68)

        # 初始化layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(head_view)  # 将 HeadView 实例添加到布局中
        self.setLayout(layout)