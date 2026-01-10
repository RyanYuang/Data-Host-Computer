import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize 
from PyQt6.QtGui import QFont,QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy ,QHBoxLayout

class HeadView(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        # 定义组件
        self.layout = None
        self.TitleLabel = None
        self.ConnectButton = None
        self.AlarmButton = None
        self.SettingButton = None

        self.InitUI()

    def InitUI(self):
        """
        @brief 初始化UI
        :return:
        """
        # 创建标签
        self.TitleLabel = QLabel(self)
        self.TitleLabel.setText("环境监测控制系统")
        Font = QFont()
        Font.setBold(True)
        Font.setPointSize(30)
        self.TitleLabel.setFont(Font)
        self.TitleLabel.setStyleSheet("""
            color: rgb(0, 0, 0);
            """)

        # 创建按钮
        self.ConnectButton = QPushButton("连接", self)
        self.ConnectButton.setStyleSheet("""
            Color:rgb(193,0,7);
            background-color: rgb(255,226,226);
            border-radius: 10px;
            width: 125px;
            height: 40px;
        """)
        self.AlarmButton = QPushButton("正常", self)
        AlarmIcon = QIcon()
        AlarmIcon.addFile("Resource/AlarmNormal.png",state=QIcon.State.Off)
        AlarmIcon.addFile("Resource/AlarmTrigger.png",state=QIcon.State.On)
        self.AlarmButton.setIcon(AlarmIcon)
        self.AlarmButton.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                height: 40px;
                width: 92px;
            }
            QPushButton:checked {
                color: rgb(193,0,7);
                background-color: rgb(255, 226, 226); /* 按下时显示红色背景 */
            }
            QPushButton:!checked 
            {
                color: rgb(74,85,101);
                background-color: rgb(243,244,246);
            }
        """)
        self.AlarmButton.setCheckable(True)

        SettingIcon = QIcon("Resource/SettingIcon.png")
        self.SettingButton = QPushButton(self)
        self.SettingButton.setIcon(SettingIcon)
        self.SettingButton.setStyleSheet("""
        QPushButton {
            width: 44px;
            height: 44px;
            border-radius: 10px;
            background-color: rgb(255,255,255);
        }
        """)

        # 创建布局
        self.layout = QHBoxLayout()
        
        # 添加标题
        self.layout.addWidget(self.TitleLabel)
        
        # 添加弹性空间，使按钮靠底部
        self.layout.addStretch()  # 或者使用这个简单的伸缩器
        
        # 添加按钮
        self.layout.addWidget(self.ConnectButton)
        self.layout.addWidget(self.AlarmButton)
        self.layout.addWidget(self.SettingButton)
        
        # 设置布局
        self.setLayout(self.layout)