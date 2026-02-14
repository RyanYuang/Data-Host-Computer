from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QTextCharFormat
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QWidget, QCheckBox,
)

from Src.MVP.base_view import BaseView


class SerialConsoleView(BaseView):
    """
    串口原始数据控制台视图 —— 右侧可折叠侧栏
    通过信号将用户操作转发给 Presenter
    """
    # ── 信号 ──
    clear_clicked = pyqtSignal()
    auto_scroll_toggled = pyqtSignal(bool)
    timestamp_toggled = pyqtSignal(bool)

    # 侧栏宽度
    PANEL_WIDTH = 380

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text_edit: QTextEdit = None
        self._line_count_label: QLabel = None

        self.setFixedWidth(self.PANEL_WIDTH)
        self._init_ui()

    # ── 由 Presenter 调用的接口 ──
    def append_line(self, formatted_line: str, direction: str = "RX"):
        """追加一行到控制台，根据方向着色"""
        fmt = QTextCharFormat()
        if direction == "TX":
            fmt.setForeground(QColor(37, 99, 235))   # 蓝色 — 发送
        elif "ERR" in formatted_line.upper():
            fmt.setForeground(QColor(220, 38, 38))    # 红色 — 错误
        else:
            fmt.setForeground(QColor(22, 163, 74))    # 绿色 — 接收

        cursor = self._text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(formatted_line + "\n", fmt)

        # 自动滚动
        if self._auto_scroll_cb.isChecked():
            self._text_edit.verticalScrollBar().setValue(
                self._text_edit.verticalScrollBar().maximum()
            )

    def update_line_count(self, count: int):
        """更新底部行计数"""
        self._line_count_label.setText(f"共 {count} 条")

    def clear_console(self):
        """清空控制台显示"""
        self._text_edit.clear()

    # ── UI 初始化 ──
    def _init_ui(self):
        self.setStyleSheet("""
            SerialConsoleView {
                background-color: rgb(30, 30, 30);
                border-left: 1px solid rgb(60, 60, 60);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # ── 顶部标题栏 ──
        header = QHBoxLayout()
        title = QLabel("📟 串口监视器")
        title.setStyleSheet("color: rgb(229, 231, 235); font-size: 15px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()

        clear_btn = QPushButton("🗑 清空")
        clear_btn.setFixedHeight(28)
        clear_btn.setStyleSheet("""
            QPushButton {
                color: rgb(209, 213, 220);
                background-color: rgb(55, 55, 55);
                border: 1px solid rgb(75, 75, 75);
                border-radius: 6px;
                padding: 2px 10px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: rgb(75, 75, 75); }
        """)
        clear_btn.clicked.connect(self.clear_clicked.emit)
        header.addWidget(clear_btn)
        layout.addLayout(header)

        # ── 文本显示区 ──
        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setFont(QFont("Menlo", 11))
        self._text_edit.setStyleSheet("""
            QTextEdit {
                background-color: rgb(24, 24, 27);
                color: rgb(212, 212, 216);
                border: 1px solid rgb(55, 55, 55);
                border-radius: 8px;
                padding: 6px;
            }
            QScrollBar:vertical {
                background: rgb(30, 30, 30);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgb(80, 80, 80);
                border-radius: 4px;
                min-height: 30px;
            }
        """)
        layout.addWidget(self._text_edit)

        # ── 底部工具栏 ──
        footer = QHBoxLayout()

        self._auto_scroll_cb = QCheckBox("自动滚动")
        self._auto_scroll_cb.setChecked(True)
        self._auto_scroll_cb.setStyleSheet("color: rgb(161, 161, 170); font-size: 12px;")
        self._auto_scroll_cb.toggled.connect(self.auto_scroll_toggled.emit)
        footer.addWidget(self._auto_scroll_cb)

        self._timestamp_cb = QCheckBox("时间戳")
        self._timestamp_cb.setChecked(True)
        self._timestamp_cb.setStyleSheet("color: rgb(161, 161, 170); font-size: 12px;")
        self._timestamp_cb.toggled.connect(self.timestamp_toggled.emit)
        footer.addWidget(self._timestamp_cb)

        footer.addStretch()

        self._line_count_label = QLabel("共 0 条")
        self._line_count_label.setStyleSheet("color: rgb(113, 113, 122); font-size: 11px;")
        footer.addWidget(self._line_count_label)

        layout.addLayout(footer)
