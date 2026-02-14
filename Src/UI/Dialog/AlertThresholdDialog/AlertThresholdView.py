from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QDoubleSpinBox, QGroupBox, QCheckBox, QDialog,
                             QPushButton, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon


class AlertThresholdView(QDialog):
    """
    告警阈值设置视图 - 提供阈值配置界面
    """
    # 定义信号
    saveClicked = pyqtSignal(dict)      # 保存按钮点击信号
    cancelClicked = pyqtSignal()        # 取消按钮点击信号
    testSoundClicked = pyqtSignal()     # 测试声音按钮点击信号
    syncClicked = pyqtSignal(dict)      # 同步到设备按钮点击信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("告警阈值设置")
        self.setMinimumSize(450, 500)
        self._presenter = None
        self._initUI()
        
    def _initUI(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 温度阈值组
        temp_group = self._createTemperatureGroup()
        main_layout.addWidget(temp_group)
        
        # 湿度阈值组
        humidity_group = self._createHumidityGroup()
        main_layout.addWidget(humidity_group)
        
        # 气体阈值组
        gas_group = self._createGasGroup()
        main_layout.addWidget(gas_group)
        
        # 光照阈值组
        light_group = self._createLightGroup()
        main_layout.addWidget(light_group)
        
        # 声音告警开关
        sound_group = self._createSoundGroup()
        main_layout.addWidget(sound_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # 同步到设备按钮
        self._sync_btn = QPushButton("📡 同步到设备")
        self._sync_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(21, 93, 252);
                color: white;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: rgb(17, 75, 202);
            }
            QPushButton:disabled {
                background-color: rgb(180, 180, 180);
            }
        """)
        self._sync_btn.clicked.connect(self._onSyncClicked)
        button_layout.addWidget(self._sync_btn)

        # 恢复默认按钮
        default_btn = QPushButton("恢复默认")
        default_btn.clicked.connect(self._onDefaultClicked)
        button_layout.addWidget(default_btn)
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self._onCancelClicked)
        button_layout.addWidget(cancel_btn)
        
        # 保存按钮
        save_btn = QPushButton("保存")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._onSaveClicked)
        button_layout.addWidget(save_btn)
        
        main_layout.addLayout(button_layout)
        
    def _createTemperatureGroup(self) -> QGroupBox:
        """创建温度阈值设置组"""
        group = QGroupBox("🌡️ 温度阈值 (°C)")
        layout = QFormLayout()
        
        # 过高告警
        self.temp_high_spin = QDoubleSpinBox()
        self.temp_high_spin.setRange(-50, 100)
        self.temp_high_spin.setDecimals(1)
        self.temp_high_spin.setSuffix(" °C")
        layout.addRow("过高告警 (>):", self.temp_high_spin)
        
        # 过低告警
        self.temp_low_spin = QDoubleSpinBox()
        self.temp_low_spin.setRange(-50, 100)
        self.temp_low_spin.setDecimals(1)
        self.temp_low_spin.setSuffix(" °C")
        layout.addRow("过低告警 (<):", self.temp_low_spin)
        
        group.setLayout(layout)
        return group
    
    def _createHumidityGroup(self) -> QGroupBox:
        """创建湿度阈值设置组"""
        group = QGroupBox("💧 湿度阈值 (%)")
        layout = QFormLayout()
        
        # 过高告警
        self.humidity_high_spin = QDoubleSpinBox()
        self.humidity_high_spin.setRange(0, 100)
        self.humidity_high_spin.setDecimals(0)
        self.humidity_high_spin.setSuffix(" %")
        layout.addRow("过高告警 (>):", self.humidity_high_spin)
        
        # 过低告警
        self.humidity_low_spin = QDoubleSpinBox()
        self.humidity_low_spin.setRange(0, 100)
        self.humidity_low_spin.setDecimals(0)
        self.humidity_low_spin.setSuffix(" %")
        layout.addRow("过低告警 (<):", self.humidity_low_spin)
        
        group.setLayout(layout)
        return group
    
    def _createGasGroup(self) -> QGroupBox:
        """创建气体阈值设置组"""
        group = QGroupBox("☠️ CO 浓度阈值 (ppm)")
        layout = QFormLayout()
        
        # 危险浓度
        self.co_danger_spin = QDoubleSpinBox()
        self.co_danger_spin.setRange(0, 1000)
        self.co_danger_spin.setDecimals(1)
        self.co_danger_spin.setSuffix(" ppm")
        layout.addRow("危险浓度 (红色警报):", self.co_danger_spin)
        
        # 警告浓度
        self.co_warning_spin = QDoubleSpinBox()
        self.co_warning_spin.setRange(0, 1000)
        self.co_warning_spin.setDecimals(1)
        self.co_warning_spin.setSuffix(" ppm")
        layout.addRow("警告浓度 (黄色警告):", self.co_warning_spin)
        
        group.setLayout(layout)
        return group
    
    def _createLightGroup(self) -> QGroupBox:
        """创建光照阈值设置组"""
        group = QGroupBox("☀️ 光照阈值 (lux)")
        layout = QFormLayout()
        
        # 过高告警
        self.light_high_spin = QDoubleSpinBox()
        self.light_high_spin.setRange(0, 100000)
        self.light_high_spin.setDecimals(0)
        self.light_high_spin.setSuffix(" lux")
        layout.addRow("光照过强 (>):", self.light_high_spin)
        
        # 过低告警
        self.light_low_spin = QDoubleSpinBox()
        self.light_low_spin.setRange(0, 100000)
        self.light_low_spin.setDecimals(0)
        self.light_low_spin.setSuffix(" lux")
        layout.addRow("光照过弱 (<):", self.light_low_spin)
        
        group.setLayout(layout)
        return group
    
    def _createSoundGroup(self) -> QGroupBox:
        """创建声音告警设置组"""
        group = QGroupBox("🔔 声音告警")
        layout = QHBoxLayout()
        
        self.sound_checkbox = QCheckBox("启用声音告警")
        self.sound_checkbox.setChecked(True)
        layout.addWidget(self.sound_checkbox)
        
        # 测试按钮
        self.test_sound_btn = QPushButton("🔊 测试声音")
        self.test_sound_btn.clicked.connect(self._onTestSoundClicked)
        layout.addWidget(self.test_sound_btn)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def set_presenter(self, presenter):
        """设置 Presenter"""
        self._presenter = presenter
        
    def load_values(self, model: dict):
        """从模型加载值到界面"""
        # 温度
        if "temperature" in model:
            self.temp_high_spin.setValue(model["temperature"].get("high", 45.0))
            self.temp_low_spin.setValue(model["temperature"].get("low", -10.0))
        
        # 湿度
        if "humidity" in model:
            self.humidity_high_spin.setValue(model["humidity"].get("high", 90.0))
            self.humidity_low_spin.setValue(model["humidity"].get("low", 20.0))
        
        # 气体
        if "co" in model:
            self.co_danger_spin.setValue(model["co"].get("danger", 50.0))
            self.co_warning_spin.setValue(model["co"].get("warning", 30.0))
        
        # 光照
        if "light" in model:
            self.light_high_spin.setValue(model["light"].get("high", 10000.0))
            self.light_low_spin.setValue(model["light"].get("low", 0.0))
        
        # 声音
        self.sound_checkbox.setChecked(model.get("sound_enabled", True))
    
    def get_values(self) -> dict:
        """从界面获取值"""
        return {
            "temperature": {
                "high": self.temp_high_spin.value(),
                "low": self.temp_low_spin.value()
            },
            "humidity": {
                "high": self.humidity_high_spin.value(),
                "low": self.humidity_low_spin.value()
            },
            "co": {
                "danger": self.co_danger_spin.value(),
                "warning": self.co_warning_spin.value()
            },
            "light": {
                "high": self.light_high_spin.value(),
                "low": self.light_low_spin.value()
            },
            "sound_enabled": self.sound_checkbox.isChecked()
        }
    
    def showEvent(self, event):
        """显示对话框时请求加载配置"""
        if self._presenter:
            self._presenter.on_view_shown()
        super().showEvent(event)
    
    def _onSaveClicked(self):
        """保存按钮点击"""
        values = self.get_values()
        self.saveClicked.emit(values)
        
    def _onCancelClicked(self):
        """取消按钮点击"""
        self.cancelClicked.emit()
        self.reject()
        
    def _onDefaultClicked(self):
        """恢复默认按钮点击"""
        if self._presenter:
            self._presenter.on_restore_default()
    
    def _onTestSoundClicked(self):
        """测试声音按钮点击"""
        self.testSoundClicked.emit()

    def _onSyncClicked(self):
        """同步到设备按钮点击"""
        values = self.get_values()
        self.syncClicked.emit(values)

    def show_sync_result(self, status: str, detail: str = ""):
        """
        显示同步结果反馈（由 Presenter 调用）。

        :param status: "waiting" | "success" | "error" | "timeout"
        :param detail: 附加说明文字
        """
        _styles = {
            "waiting": ("⏳ 同步中…", """
                QPushButton {
                    background-color: rgb(245, 158, 11);
                    color: white;
                    border-radius: 6px;
                    padding: 6px 16px;
                }
            """),
            "success": ("✅ 已同步", """
                QPushButton {
                    background-color: rgb(22, 163, 74);
                    color: white;
                    border-radius: 6px;
                    padding: 6px 16px;
                }
            """),
            "error": ("❌ 同步失败", """
                QPushButton {
                    background-color: rgb(220, 38, 38);
                    color: white;
                    border-radius: 6px;
                    padding: 6px 16px;
                }
            """),
            "timeout": ("⚠️ 设备无响应", """
                QPushButton {
                    background-color: rgb(234, 88, 12);
                    color: white;
                    border-radius: 6px;
                    padding: 6px 16px;
                }
            """),
        }

        text, style = _styles.get(status, _styles["error"])
        self._sync_btn.setText(text)
        self._sync_btn.setStyleSheet(style)
        self._sync_btn.setEnabled(status != "waiting")   # 等待中禁用按钮

        if detail:
            self._sync_btn.setToolTip(detail)
            print(f"[AlertThresholdView] 同步状态={status}: {detail}")

        # 非等待状态 → 3 秒后恢复按钮原样
        if status != "waiting":
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(3000, self._resetSyncBtn)

    def _resetSyncBtn(self):
        """恢复同步按钮原始样式"""
        self._sync_btn.setText("📡 同步到设备")
        self._sync_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(21, 93, 252);
                color: white;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: rgb(17, 75, 202);
            }
            QPushButton:disabled {
                background-color: rgb(180, 180, 180);
            }
        """)
