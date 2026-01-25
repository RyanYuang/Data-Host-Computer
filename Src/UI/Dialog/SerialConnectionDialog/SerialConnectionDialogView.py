from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton
from Src.UI.Components.ComboBoxWithTitle import ComboBoxWithTitle
from Src.Serial.SerialManger import SerialManger


class SeireConnectionDialogView(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        # 隐藏系统标题栏，但保持对话框行为
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Dialog
        )
        self.setModal(True)  # 设置为模态对话框
        self.resize(672, 320)
        
        # 初始化串口管理器
        self.serial_manager = SerialManger()
        
        # 创建定时器，每1秒刷新一次串口列表
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_serial_ports)
        self.refresh_timer.setInterval(1000)  # 1000毫秒 = 1秒
        
        # 保存port_combo引用，以便更新
        self.port_combo = None
        self.setStyleSheet("""
            background-color: transparent;
            
        """)
        
        # Main container widget with rounded corners
        self.main_container = QWidget(self)
        self.main_container.setObjectName("main_container")
        self.main_container.setStyleSheet("""
        #main_container {
                background-color: rgb(255, 255, 255);  
                border-radius: 16px;                          
                border: 1px solid rgb(220, 220, 220);
            }  
        """)

        # Main layout for dialog
        self.dialog_layout = QVBoxLayout(self)
        self.dialog_layout.setContentsMargins(0, 0, 0, 0)
        self.dialog_layout.addWidget(self.main_container)
        
        # Layout for container content
        self.layout = QVBoxLayout(self.main_container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Head
        self.titleWidget = QWidget(self.main_container)
        self.titleWidget.setLayout(QHBoxLayout())
        self.titleWidget.layout().setContentsMargins(20, 20, 20, 20)

        self.icon_label = QLabel(self.titleWidget)
        pixmap = QPixmap("Resource/Connection Dialog Iocn.png")
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = QLabel(self.titleWidget)
        self.title.setText("串口连接配置")
        self.title.setStyleSheet("""
            color: rgb(0, 0, 0);
        """)
        self.titleWidget.layout().addWidget(self.icon_label)
        self.titleWidget.layout().addWidget(self.title)
        self.titleWidget.layout().addStretch()  # Push close button to the right
        
        # Close button
        self.close_button = QPushButton("×", self.main_container)
        self.close_button.setFixedSize(32, 32)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 16px;
                color: rgb(0, 0, 0);
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(240, 240, 240);
            }
            QPushButton:pressed {
                background-color: rgb(220, 220, 220);
            }
        """)
        self.close_button.clicked.connect(self.close)
        self.titleWidget.layout().addWidget(self.close_button)

        # combo组件
        self.combocontainer = QWidget(self.main_container)
        self.combocontainer.setLayout(QVBoxLayout())
        self.combocontainer.layout().setContentsMargins(24, 24,24, 33)
        self.combocontainer.setObjectName("combocontainer")
        self.combocontainer.setStyleSheet("""
            #combocontainer
            {
                border: 1px solid rgb(229, 231, 235);
            }
        """)
        
        # 串口选择 - 使用通用组件
        self.port_combo = ComboBoxWithTitle(
            self.main_container,
            title="串口选择",
            items=["Empty"],
            callback=self.on_port_selected_callback
        )
        self.combocontainer.layout().addWidget(self.port_combo)
        
        # 立即刷新一次串口列表
        self.refresh_serial_ports()

        # 确认以及取消组件
        self.confirmAndCancelWidget = QWidget(self.main_container)
        self.confirmAndCancelWidget.setObjectName("confirmAndCancelWidget")
        self.confirmAndCancelWidget.setStyleSheet("""
            #confirmAndCancelWidget
            {
                background-color: rgb(249, 250, 251);
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }
        """)
        self.confirmAndCancelWidget.setLayout(QHBoxLayout())

        # 取消按钮
        self.cancelBtn = QPushButton(self.confirmAndCancelWidget)
        self.cancelBtn.setMinimumSize(306,46)
        self.cancelBtn.setStyleSheet("""
            border: 1px solid rgb(229, 231, 235);
            border-radius: 10px;
            color: rgb(54, 65, 83);
        """)
        self.cancelBtn.setText("取消")

        # 连接按钮
        self.confirmBtn = QPushButton(self.confirmAndCancelWidget)
        self.confirmBtn.setMinimumSize(306,46)
        self.confirmBtn.setStyleSheet("""
            border-radius: 10px;
            background-color: rgb(79, 57, 246);
        """)
        self.confirmBtn.setText("连接设备")
        self.confirmAndCancelWidget.layout().addWidget(self.cancelBtn)
        self.confirmAndCancelWidget.layout().addWidget(self.confirmBtn)


        self.layout.addWidget(self.titleWidget)
        self.layout.addWidget(self.combocontainer)
        self.layout.addWidget(self.confirmAndCancelWidget)
        
        # 连接关闭信号，停止定时器
        self.finished.connect(self.on_dialog_closed)
    
    def on_port_selected_callback(self, selected_text):
        """串口选择回调函数"""
        print(f"选中的串口: {selected_text}")
    
    def refresh_serial_ports(self):
        """刷新串口列表"""
        try:
            # 获取当前选中的串口（如果有）
            current_selection = self.port_combo.getCurrentText() if self.port_combo else ""
            
            # 获取串口列表
            serial_ports = self.serial_manager.GetSerialList()
            
            # 将串口对象转换为字符串列表
            port_names = []
            for port in serial_ports:
                port_name = port.device
                port_names.append(port_name)
            
            # 如果没有串口，显示提示信息
            if not port_names:
                port_names = ["未检测到串口"]
            
            # 更新ComboBox的选项
            if self.port_combo:
                self.port_combo.setItems(port_names)
                
                # 如果之前选中的串口仍然存在，恢复选择
                if current_selection and current_selection in port_names:
                    self.port_combo.setCurrentText(current_selection)
                elif port_names and port_names[0] != "未检测到串口":
                    # 否则选择第一个可用串口
                    self.port_combo.setCurrentIndex(0)
        except Exception as e:
            print(f"刷新串口列表时出错: {e}")
    
    def showEvent(self, event):
        """对话框显示时启动定时器"""
        super().showEvent(event)
        self.refresh_timer.start()
    
    def on_dialog_closed(self, result):
        """对话框关闭时停止定时器"""
        self.refresh_timer.stop()
    def set_presenter(self,presenter):
        self._presenter = presenter