from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout

from Src.MVP.base_view import BaseView

class DataMonitorView(BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_widgets = []  # To store references to the data value labels
        self.item_widgets = []  # To store references to the item container widgets
        self._blink_timers = {}  # QTimer for each blinking item

    def init_ui(self, data_items):
        """
        Initializes the user interface based on a list of data items.
        The view is built once and only the values are updated later.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Title
        title_label = QLabel("数据监控", self)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(20)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgb(0, 0, 0);")
        layout.addWidget(title_label)

        # Container for data items
        container = QWidget(self)
        container.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        container.setMinimumSize(1125, 176)
        container_layout = QHBoxLayout()
        container.setLayout(container_layout)

        # Create UI for each data item
        for item in data_items:
            item_widget = QWidget(self)
            item_widget.setLayout(QVBoxLayout())
            item_widget.setFixedSize(288, 176)
            item_widget.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 16px;")

            # Icon
            icon_label = QLabel(item_widget)
            pixmap = QIcon(item.icon_path).pixmap(48, 48)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Name
            name_label = QLabel(item.name, item_widget)
            name_label.setStyleSheet("font-size: 14px; color: rgb(74,85,101)")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Data Value (this is the dynamic part)
            data_label = QLabel(str(item.data_value), item_widget) # Initial value
            data_label.setStyleSheet("color: blue; font-size: 36px; font-weight: bold;")
            data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.data_widgets.append(data_label) # Store reference to update later

            # Add widgets to item layout
            item_layout = item_widget.layout()
            item_layout.addWidget(icon_label)
            item_layout.addWidget(name_label)
            item_layout.addStretch()
            item_layout.addWidget(data_label)
            item_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            # Store reference to item widget for background color changes
            self.item_widgets.append(item_widget)
            container_layout.addWidget(item_widget)

        layout.addWidget(container)

    def update_value_at(self, index: int, value):
        """Updates the text of a data label at a specific index."""
        if 0 <= index < len(self.data_widgets):
            # Ensure value is a string for the QLabel
            self.data_widgets[index].setText(str(value))
        else:
            print(f"Error: View tried to update widget at invalid index {index}")
    
    def start_blink(self, index: int):
        """开始闪烁指定索引的数据项背景"""
        if not (0 <= index < len(self.item_widgets)):
            return
        
        # 如果已经在闪烁，不重复创建定时器
        if index in self._blink_timers:
            return
        
        from PyQt6.QtCore import QTimer
        item_widget = self.item_widgets[index]
        
        # 闪烁状态
        blink_state = {'is_red': False}
        
        def toggle_color():
            if blink_state['is_red']:
                # 恢复正常白色背景
                item_widget.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 16px;")
            else:
                # 红色背景
                item_widget.setStyleSheet("background-color: rgb(255, 100, 100); border-radius: 16px;")
            blink_state['is_red'] = not blink_state['is_red']
        
        # 创建定时器，每500ms切换一次颜色
        timer = QTimer(self)
        timer.timeout.connect(toggle_color)
        timer.start(500)
        self._blink_timers[index] = timer
    
    def stop_blink(self, index: int):
        """停止闪烁并恢复正常背景"""
        if index in self._blink_timers:
            self._blink_timers[index].stop()
            del self._blink_timers[index]
        
        if 0 <= index < len(self.item_widgets):
            # 恢复正常白色背景
            self.item_widgets[index].setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 16px;")
    
    def stop_all_blink(self):
        """停止所有闪烁"""
        for index in list(self._blink_timers.keys()):
            self.stop_blink(index)

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter = presenter
