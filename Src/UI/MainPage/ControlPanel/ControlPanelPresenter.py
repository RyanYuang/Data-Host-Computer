from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager
from Src.Serial.SerialManager import SerialManager

from .ControlPanelModel import ControlPanelModel
from .ControlPanelView import ControlPanelView

# 子模块 MVP
from .DirectionControlPanel.DirectionControlPanelModel import DirectionControlPanelModel
from .DirectionControlPanel.DirectionControlPanelPresenter import DirectionControlPanelPresenter
from .SpeedControl.SpeedControlModel import SpeedControlModel
from .SpeedControl.SpeedControlPresenter import SpeedControlPresenter


class ControlPanelPresenter(BasePresenter, MessageHandler):
    """
    控制面板 Presenter
    职责：
    1. 组装子模块（方向控制、速度控制）的 MVP
    2. 监听串口连接状态，更新 View 的启用/禁用
    """
    def __init__(self, view: ControlPanelView, model: ControlPanelModel,
                 message_manager: MessageManager):
        super().__init__(view, model)
        self._model = model
        self._message_manager = message_manager

        # ── 组装子模块 MVP ──
        # 方向控制
        direction_model = DirectionControlPanelModel()
        self._direction_presenter = DirectionControlPanelPresenter(
            view=view.direction_panel_view,
            model=direction_model,
        )

        # 速度控制
        speed_model = SpeedControlModel()
        self._speed_presenter = SpeedControlPresenter(
            view=view.speed_control_view,
            model=speed_model,
        )

        # 注册消息处理
        self._message_manager.register(self)

        # 读取当前串口状态以初始化 UI
        serial_status = SerialManager().GetSerialStatus()
        self._model.is_serial_connected = serial_status
        self._view.set_connected(serial_status)

    def handle(self, message: Message) -> HandleResult:
        """监听连接状态变更"""
        if message.type == "serial.connection.status":
            connected = message.payload
            self._model.is_serial_connected = connected
            self._view.set_connected(connected)
            return HandleResult.CONTINUE  # 让其他 handler 也能收到
        return HandleResult.SKIP
