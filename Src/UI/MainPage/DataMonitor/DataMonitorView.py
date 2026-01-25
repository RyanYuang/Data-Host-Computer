from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout

from Src.MVP.base_view import BaseView

class DataMonitorView(BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_widgets = []  # To store references to the data value labels

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

            container_layout.addWidget(item_widget)

        layout.addWidget(container)

    def update_value_at(self, index: int, value):
        """Updates the text of a data label at a specific index."""
        if 0 <= index < len(self.data_widgets):
            # Ensure value is a string for the QLabel
            self.data_widgets[index].setText(str(value))
        else:
            print(f"Error: View tried to update widget at invalid index {index}")

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter = presenter
