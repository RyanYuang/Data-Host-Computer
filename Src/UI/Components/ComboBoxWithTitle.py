from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from typing import List, Callable, Optional


class ComboBoxWithTitle(QWidget):
    """
    通用组件：带标题的 ComboBox
    支持设置标题、选项列表和回调函数
    """
    
    def __init__(self, parent=None, title: str = "", items: List[str] = None, callback: Optional[Callable] = None):
        """
        初始化带标题的 ComboBox 组件
        
        Args:
            parent: 父组件
            title: 标题文本
            items: ComboBox 的选项列表
            callback: 选择改变时的回调函数，接收一个参数：选中的文本
        """
        super().__init__(parent)
        
        self.title_label = None
        self.combobox = None
        self.callback = callback
        
        self.initUI()
        
        print(f"After initUI: self.combobox = {self.combobox}, id={id(self.combobox)}")
        
        # 设置初始值
        if title:
            self.setTitle(title)
        if items:
            print(f"About to call setItems with items={items}")
            self.setItems(items)
        if callback:
            self.setCallback(callback)
    
    def initUI(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 创建标题标签
        self.title_label = QLabel(self)
        self.title_label.setStyleSheet("color: rgb(0, 0, 0);")
        layout.addWidget(self.title_label)
        
        # 创建 ComboBox
        self.combobox = QComboBox(self)
        print(f"initUI: combobox created, id={id(self.combobox)}")
        self.combobox.setEditable(False)  # 确保不可编辑
        self.combobox.setMinimumHeight(36)
        self.combobox.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                background-color: rgb(255, 255, 255);
                border: 1px solid rgb(209, 213, 220);
                padding: 8px;
                min-height: 36px;
                color:rgb(0,0,0)
            }
            QComboBox:hover {
                border: 1px solid rgb(21, 93, 252);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid rgb(209, 213, 220);
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                color: rgb(0, 0, 0);
            }
            QComboBox::drop-down:hover {
                border-left: 1px solid rgb(21, 93, 252);
            }
            QComboBox QAbstractItemView {
                border: 1px solid rgb(209, 213, 220);
                border-radius: 8px;
                background-color: rgb(255, 255, 255);
                selection-background-color: rgb(21, 93, 252);
                selection-color: rgb(255, 255, 255);
                color: rgb(0, 0, 0);
            }
        """)
        
        # 连接信号
        self.combobox.currentTextChanged.connect(self._onTextChanged)
        
        layout.addWidget(self.combobox)
    
    def setTitle(self, title: str):
        """
        设置标题文本
        
        Args:
            title: 标题文本
        """
        if self.title_label:
            self.title_label.setText(title)
    
    def getTitle(self) -> str:
        """
        获取标题文本
        
        Returns:
            标题文本
        """
        return self.title_label.text() if self.title_label else ""
    
    def setItems(self, items: List[str]):
        """
        设置 ComboBox 的选项列表
        
        Args:
            items: 选项列表
        """
        print(f"setItems called")
        print(f"  self.combobox = {self.combobox}")
        print(f"  type(self.combobox) = {type(self.combobox)}")
        print(f"  bool(self.combobox) = {bool(self.combobox)}")
        print(f"  self.combobox is None = {self.combobox is None}")
        if self.combobox is not None:
            try:
                self.combobox.clear()
                self.combobox.addItems(items)
                print(f"Items added successfully, count={self.combobox.count()}")
            except Exception as e:
                print(f"Error adding items: {e}")
        else:
            print("combobox is None!")
    
    def getItems(self) -> List[str]:
        """
        获取 ComboBox 的所有选项
        
        Returns:
            选项列表
        """
        if self.combobox:
            return [self.combobox.itemText(i) for i in range(self.combobox.count())]
        return []
    
    def setCurrentText(self, text: str):
        """
        设置当前选中的文本
        
        Args:
            text: 要选中的文本
        """
        if self.combobox:
            index = self.combobox.findText(text)
            if index >= 0:
                self.combobox.setCurrentIndex(index)
    
    def getCurrentText(self) -> str:
        """
        获取当前选中的文本
        
        Returns:
            当前选中的文本
        """
        return self.combobox.currentText() if self.combobox else ""
    
    def setCurrentIndex(self, index: int):
        """
        设置当前选中的索引
        
        Args:
            index: 索引值
        """
        if self.combobox and 0 <= index < self.combobox.count():
            self.combobox.setCurrentIndex(index)
    
    def getCurrentIndex(self) -> int:
        """
        获取当前选中的索引
        
        Returns:
            当前选中的索引
        """
        return self.combobox.currentIndex() if self.combobox else -1
    
    def setCallback(self, callback: Optional[Callable]):
        """
        设置选择改变时的回调函数
        
        Args:
            callback: 回调函数，接收一个参数：选中的文本
        """
        self.callback = callback
    
    def _onTextChanged(self, text: str):
        """
        内部方法：处理 ComboBox 文本改变事件
        
        Args:
            text: 选中的文本
        """
        if self.callback:
            self.callback(text)
    
    def clear(self):
        """清空所有选项"""
        if self.combobox:
            self.combobox.clear()
