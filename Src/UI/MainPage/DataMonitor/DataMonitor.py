import PyQt6
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout


# 定义数据项结构体类
class DataItem:
    def __init__(self, icon_path, name, data_value):
        self.icon_path = icon_path  # 图标路径
        self.name = name            # 数据名称
        self.data_value = data_value  # 实际数据值


class DataMonitor(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        # 类似C语言结构体数组的数据结构
        self.data_array = []
        
        # 初始化示例数据
        self.initData()
        self.initUI()
    
    def initData(self):
        """初始化数据数组"""
        # 添加示例数据项
        self.data_array.append(DataItem("Resource/Tempreture.png", "温度", 25.6))
        self.data_array.append(DataItem("Resource/Humidity.png", "湿度", 60.3))
        self.data_array.append(DataItem("Resource/CO.png", "一氧化碳", 0.5))
        self.data_array.append(DataItem("Resource/Light.png", "光照", 450))
    
    def initUI(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(0)

        # 标题
        title_label = QLabel("数据监控", self)
        title_font = QFont()

        title_font.setBold(True)
        title_font.setPointSize(20)
        title_label.setFont(title_font)
        title_label.setStyleSheet(
            """ color: rgb(0, 0, 0);"""
        )
        layout.addWidget(title_label)

        container = QWidget(self)
        container.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        container.setMinimumSize(1125,176)
        container.setLayout(QHBoxLayout())
        
        # 创建数据项的UI
        datacontainer = []
        for i, data_item in enumerate(self.data_array):
            datacontainer.append(QWidget(self))
            datacontainer[i].setLayout(QVBoxLayout())
            datacontainer[i].setFixedSize(288, 176)  # 使用 setFixedSize 而不是 resize
            datacontainer[i].setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 16px;")
            
            # 图标
            icon_label = QLabel(datacontainer[i])
            icon = QIcon(data_item.icon_path)
            pixmap = icon.pixmap(48, 48)  # 调整图标大小
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
            
            # 名称
            name_label = QLabel(data_item.name, datacontainer[i])
            name_label.setStyleSheet("font-size: 14px; color: rgb(74,85,101)")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 数据值
            data_label = QLabel(str(data_item.data_value), datacontainer[i])
            data_label.setStyleSheet("color: blue; font-size: 36px; font-weight: bold;")
            data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 添加到布局 - 修正：只添加一次每个控件
            datacontainer[i].layout().addWidget(icon_label)
            datacontainer[i].layout().addWidget(name_label)
            datacontainer[i].layout().addStretch()  # 添加弹性空间
            datacontainer[i].layout().addWidget(data_label)
            datacontainer[i].layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
            container.layout().addWidget(datacontainer[i])

        # 将容器添加到主布局
        layout.addWidget(container)
        self.setLayout(layout)
    
    def update_data(self, index, new_value):
        """更新指定索引的数据值"""
        if 0 <= index < len(self.data_array):
            self.data_array[index].data_value = new_value
            
            # 注意：这里需要更新UI显示，可以通过重新构建UI或找到对应的label来更新
            # 为简化，这里只是更新数据，实际应用中可能需要更复杂的UI更新逻辑
            self.update()
    
    def get_data_by_name(self, name):
        """根据名称获取数据值"""
        for item in self.data_array:
            if item.name == name:
                return item.data_value
        return None
    
    def add_data_item(self, icon_path, name, data_value):
        """添加新的数据项"""
        new_item = DataItem(icon_path, name, data_value)
        self.data_array.append(new_item)
    
    def get_all_data(self):
        """获取所有数据项"""
        return self.data_array