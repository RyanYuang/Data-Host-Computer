from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout

from Src.MVP.base_view import BaseView


class DirectionControlPanelView(BaseView):
    def __init__(self, parent=None):
        super(DirectionControlPanelView, self).__init__(parent)
        self.setMinimumSize(QSize(256, 300))
        self.init_ui()
        self.setStyleSheet("""
            QPushButton{
                background-color:rgb(255, 255, 255);
                border-radius:10px;
                height:46px;
                width:46px;
            }
            background-color:rgb(0, 0, 255);
        """)

    def init_ui(self):
        main_container = QWidget(self)
        main_container.setMinimumSize(QSize(256, 300))
        main_container.setStyleSheet("""
            QPushButton{
                color:rgb(106, 114, 130);
                background-color:rgb(209, 213, 220);
            }
            QPushButton:click {
                background-color:rgb(165, 169, 175);
            }
        """)
        layout = QGridLayout()
        self.left_btn = QPushButton("Left")
        self.left_btn.setMinimumSize(QSize(80, 64))
        self.left_btn.setStyleSheet("""
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
        """)
        self.right_btn = QPushButton("Right")
        self.right_btn.setMinimumSize(QSize(80, 64))
        self.right_btn.setStyleSheet("""
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        self.up_btn = QPushButton("Up")
        self.up_btn.setMinimumSize(QSize(64, 80))
        self.up_btn.setStyleSheet("""
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        self.down_btn = QPushButton("Down")
        self.down_btn.setMinimumSize(QSize(20, 80))
        self.down_btn.setStyleSheet("""
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        self.mid_btn = QPushButton("Stop")
        self.mid_btn.setMinimumSize(QSize(80, 80))
        self.mid_btn.setStyleSheet("""
            border-radius: 40px
        """)
        layout.addWidget(self.up_btn, 0, 1)
        layout.addWidget(self.left_btn, 1, 0)
        layout.addWidget(self.mid_btn, 1, 1)
        layout.addWidget(self.right_btn, 1, 2)
        layout.addWidget(self.down_btn, 2, 1)
        main_container.setLayout(layout)
        parent_layout = QVBoxLayout(self)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_layout.addWidget(main_container)

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter = presenter
        self.left_btn.clicked.connect(self._presenter.left_btn_clicked)
        self.right_btn.clicked.connect(self._presenter.right_btn_clicked)
        self.up_btn.clicked.connect(self._presenter.up_btn_clicked)
        self.down_btn.clicked.connect(self._presenter.down_btn_clicked)
        self.mid_btn.clicked.connect(self._presenter.mid_btn_clicked)


