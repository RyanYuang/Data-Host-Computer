from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton
from Src.UI.Components.ComboBoxWithTitle import ComboBoxWithTitle
from Src.Serial.SerialManger import SerialManger


class SeireConnectionDialog(QDialog):
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
        main_container = QWidget(self)
        main_container.setObjectName("main_container")
        main_container.setStyleSheet("""
        #main_container {
                background-color: rgb(255, 255, 255);  
                border-radius: 16px;                          
                border: 1px solid rgb(220, 220, 220);
            }  
        """)

        # Main layout for dialog
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(main_container)
        
        # Layout for container content
        layout = QVBoxLayout(main_container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Head
        titleWidget = QWidget(main_container)
        titleWidget.setLayout(QHBoxLayout())
        titleWidget.layout().setContentsMargins(20, 20, 20, 20)

        icon_label = QLabel(titleWidget)
        pixmap = QPixmap("Resource/Connection Dialog Iocn.png")
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel(titleWidget)
        title.setText("串口连接配置")
        title.setStyleSheet("""
            color: rgb(0, 0, 0);
        """)
        titleWidget.layout().addWidget(icon_label)
        titleWidget.layout().addWidget(title)
        titleWidget.layout().addStretch()  # Push close button to the right
        
        # Close button
        close_button = QPushButton("×", main_container)
        close_button.setFixedSize(32, 32)
        close_button.setStyleSheet("""
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
        close_button.clicked.connect(self.close)
        titleWidget.layout().addWidget(close_button)

        # combo组件
        combocontainer = QWidget(main_container)
        combocontainer.setLayout(QVBoxLayout())
        combocontainer.layout().setContentsMargins(24, 24,24, 33)
        combocontainer.setObjectName("combocontainer")
        combocontainer.setStyleSheet("""
            #combocontainer
            {
                border: 1px solid rgb(229, 231, 235);
            }
        """)
        
        # 串口选择 - 使用通用组件
        def on_port_selected(selected_text):
            """串口选择回调函数"""
            print(f"选中的串口: {selected_text}")
        
        self.port_combo = ComboBoxWithTitle(
            main_container,
            title="串口选择",
            items=["Empty"],
            callback=on_port_selected
        )
        combocontainer.layout().addWidget(self.port_combo)
        
        # 立即刷新一次串口列表
        self.refresh_serial_ports()

        # 确认以及取消组件
        confirmAndCancelWidget = QWidget(main_container)
        confirmAndCancelWidget.setObjectName("confirmAndCancelWidget")
        confirmAndCancelWidget.setStyleSheet("""
            #confirmAndCancelWidget
            {
                background-color: rgb(249, 250, 251);
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }
        """)
        confirmAndCancelWidget.setLayout(QHBoxLayout())

        # 取消按钮
        cancelBtn = QPushButton(confirmAndCancelWidget)
        cancelBtn.setMinimumSize(306,46)
        cancelBtn.setStyleSheet("""
            border: 1px solid rgb(229, 231, 235);
            border-radius: 10px;
            color: rgb(54, 65, 83);
        """)
        cancelBtn.setText("取消")

        # 连接按钮
        confirmBtn = QPushButton(confirmAndCancelWidget)
        confirmBtn.setMinimumSize(306,46)
        confirmBtn.setStyleSheet("""
            border-radius: 10px;
            background-color: rgb(79, 57, 246);
        """)
        confirmBtn.setText("连接设备")
        confirmAndCancelWidget.layout().addWidget(cancelBtn)
        confirmAndCancelWidget.layout().addWidget(confirmBtn)


        layout.addWidget(titleWidget)
        layout.addWidget(combocontainer)
        layout.addWidget(confirmAndCancelWidget)
        
        # 连接关闭信号，停止定时器
        self.finished.connect(self.on_dialog_closed)
    
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
                port_name = port.portName()
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