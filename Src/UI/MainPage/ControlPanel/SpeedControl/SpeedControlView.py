from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QButtonGroup

from Src.MVP.base_view import BaseView


class SpeedControlView(BaseView):
    """
    速度控制视图层 —— 纯 UI
    通过信号将用户操作转发给 Presenter
    """
    # 信号：用户点击了速度按钮，参数为按钮索引
    speed_btn_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons = []
        self._button_group: QButtonGroup = None
        self._init_ui()

    def init_speed_buttons(self, labels: list[str]):
        """由 Presenter 调用，根据 Model 的档位列表初始化按钮文本"""
        for i, label in enumerate(labels):
            if i < len(self._buttons):
                self._buttons[i].setText(label)

    # ── UI 初始化 ──
    def _init_ui(self):
        main_container = QWidget(self)
        main_container.setMinimumSize(QSize(200, 300))

        layout = QHBoxLayout()
        self._button_group = QButtonGroup(self)

        # 先创建 4 个占位按钮（文本由 Presenter 填充）
        for i in range(4):
            btn = QPushButton("")
            btn.setCheckable(True)
            btn.setMinimumSize(QSize(137, 36))
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 10px;
                    background-color: rgb(243, 244, 246);
                    color: rgb(0, 0, 0);
                }
                QPushButton:checked {
                    background-color: rgb(21, 93, 252);
                    color: rgb(255, 255, 255);
                }
            """)
            self._button_group.addButton(btn, i)
            self._buttons.append(btn)
            layout.addWidget(btn)

        main_container.setLayout(layout)

        parent_layout = QVBoxLayout(self)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(main_container)

        # 将按钮组信号转发为自定义信号
        self._button_group.idClicked.connect(self.speed_btn_clicked.emit)
