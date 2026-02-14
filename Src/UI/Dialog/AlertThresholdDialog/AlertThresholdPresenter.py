from PyQt6.QtCore import QTimer

from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager
from Src.Serial.SerialManager import SerialManager
from .AlertThresholdModel import AlertThresholdModel
from .AlertThresholdView import AlertThresholdView


class AlertThresholdPresenter(BasePresenter, MessageHandler):
    """
    告警阈值设置Presenter - 处理告警配置的业务逻辑
    """
    def __init__(self, view: AlertThresholdView, model: AlertThresholdModel, 
                 message_manager: MessageManager):
        super().__init__(view)
        self._model = model
        self._message_manager = message_manager
        
        # 注册为消息处理器
        self._message_manager.register(self)
        
        # 设置视图的presenter
        view.set_presenter(self)
        
        # 串口管理器（用于同步阈值到下位机）
        self._serial_manager = SerialManager()

        # 连接视图信号
        view.saveClicked.connect(self._on_save)
        view.cancelClicked.connect(self._on_cancel)
        view.testSoundClicked.connect(self._on_test_sound)
        view.syncClicked.connect(self._on_sync)

        # ── 同步反馈超时定时器 ──
        self._sync_timeout_timer = QTimer()
        self._sync_timeout_timer.setSingleShot(True)
        self._sync_timeout_timer.timeout.connect(self._on_sync_timeout)
        self._waiting_for_sync_response = False
        
        # 加载保存的配置
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        # 从文件加载配置
        self._model.load_from_file()
        
        # 更新视图显示
        self._view.load_values(self._model.to_dict())
    
    def on_view_shown(self):
        """视图显示时刷新配置"""
        self._model.load_from_file()
        self._view.load_values(self._model.to_dict())
    
    def on_restore_default(self):
        """恢复默认配置"""
        # 创建新模型（使用默认值）
        default_model = AlertThresholdModel()
        self._view.load_values(default_model.to_dict())
    
    def _on_save(self, values: dict):
        """保存配置"""
        # 更新模型
        self._update_model_from_values(values)
        
        # 保存到文件
        if self._model.save_to_file():
            # 发送配置更新消息
            self._message_manager.dispatch(
                Message("alert.config.updated", self._model.to_dict())
            )
            self._view.accept()  # 关闭对话框
        else:
            # 保存失败，发送错误消息
            self._message_manager.dispatch(
                Message("alert.config.save_failed", {"error": "保存配置文件失败"})
            )
    
    def _on_cancel(self):
        """取消操作"""
        # 发送取消消息
        self._message_manager.dispatch(Message("alert.config.cancelled"))
    
    def _on_test_sound(self):
        """测试声音按钮点击"""
        print("[AlertThresholdPresenter] 测试警告声音")
        self._message_manager.dispatch(
            Message("alert.sound.play", {"level": "warning"})
        )

    def _on_sync(self, values: dict):
        """
        将当前界面上的阈值同步到下位机。

        流程：
        1. 先将界面值写入 Model
        2. 通过 Model.build_sync_command() 生成指令
        3. 通过 SerialManager 发送
        4. 进入等待状态，启动 3 秒超时定时器
        5. 由 handle() 接收 serial.config.response 消息后显示结果
        """
        # 1. 更新 Model
        self._update_model_from_values(values)

        # 2. 检查串口连接
        if not self._serial_manager.GetSerialStatus():
            print("[AlertThresholdPresenter] 串口未连接，无法同步")
            self._view.show_sync_result("error", "串口未连接")
            return

        # 3. 构建并发送指令
        cmd = self._model.build_sync_command()
        print(f"[AlertThresholdPresenter] 同步阈值指令: {cmd}")
        success = self._serial_manager.write(cmd)

        if not success:
            self._view.show_sync_result("error", "串口写入失败")
            return

        # 4. 发送成功 → 进入等待反馈状态
        self._waiting_for_sync_response = True
        self._view.show_sync_result("waiting", "等待设备响应…")
        self._sync_timeout_timer.start(3000)   # 3 秒超时

        # 派发 TX 消息供 SerialConsole 显示
        self._message_manager.dispatch(
            Message("serial.data.tx", {"data": cmd.decode('ascii').strip()})
        )

    def _on_sync_timeout(self):
        """3 秒内未收到设备反馈"""
        if self._waiting_for_sync_response:
            self._waiting_for_sync_response = False
            print("[AlertThresholdPresenter] 同步超时，设备无响应")
            self._view.show_sync_result("timeout", "设备无响应（3 秒超时）")

    def _update_model_from_values(self, values: dict):
        """从视图值更新模型"""
        if "temperature" in values:
            self._model.temp_high = values["temperature"]["high"]
            self._model.temp_low = values["temperature"]["low"]
            
        if "humidity" in values:
            self._model.humidity_high = values["humidity"]["high"]
            self._model.humidity_low = values["humidity"]["low"]
            
        if "co" in values:
            self._model.co_danger = values["co"]["danger"]
            self._model.co_warning = values["co"]["warning"]
            
        if "light" in values:
            self._model.light_high = values["light"]["high"]
            self._model.light_low = values["light"]["low"]
            
        self._model.sound_enabled = values.get("sound_enabled", True)
    
    def handle(self, message: Message) -> HandleResult:
        """
        处理来自其他模块的消息
        """
        # ── 处理阈值配置同步反馈 ──
        if message.type == "serial.config.response":
            if self._waiting_for_sync_response:
                self._waiting_for_sync_response = False
                self._sync_timeout_timer.stop()

                success = message.payload.get("success", False)
                detail = message.payload.get("detail", "")

                if success:
                    self._view.show_sync_result("success", f"✓ {detail}")
                    self._message_manager.dispatch(
                        Message("alert.config.synced", self._model.to_dict())
                    )
                else:
                    self._view.show_sync_result("error", detail)

            return HandleResult.CONSUMED

        # 处理传感器数据更新，检查是否触发告警
        if message.type == "sensor.data.updated":
            data = message.payload
            
            # 获取当前传感器数据
            temperature = data.get("temperature", 0)
            humidity = data.get("humidity", 0)
            co_level = data.get("co", 0)
            light = data.get("light", 0)
            
            # 检查告警
            result = self._model.check_alerts(temperature, humidity, co_level, light)
            
            if result["count"] > 0:
                # 有告警，发送告警消息
                for alert in result["alerts"]:
                    self._message_manager.dispatch(
                        Message("alert.triggered", alert)
                    )
                    
                    # 如果启用声音告警
                    if self._model.sound_enabled and alert["level"] in ["danger", "warning"]:
                        self._message_manager.dispatch(
                            Message("alert.sound.play", {"level": alert["level"]})
                        )
            
            return HandleResult.CONSUMED
        
        # 处理获取当前阈值配置的请求
        elif message.type == "alert.config.get":
            self._message_manager.dispatch(
                Message("alert.config.response", self._model.to_dict())
            )
            return HandleResult.CONSUMED
        
        # 不处理其他消息
        return HandleResult.SKIP
