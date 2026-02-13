from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager

from .MainPageModel import MainPageModel
from .MainPage import MainPageView

# 子模块 MVP
from .Head.HeadModel import HeadModel
from .Head.HeadPresenter import HeadPresenter
from .DataMonitor.DataMonitorModel import DataMonitorModel
from .DataMonitor.DataMonitorPresenter import DataMonitorPresenter
from .ControlPanel.ControlPanelModel import ControlPanelModel
from .ControlPanel.ControlPanelPresenter import ControlPanelPresenter


class MainPagePresenter(BasePresenter, MessageHandler):
    """
    MainPage Presenter —— 负责：
    1. 组装所有子模块的 MVP 三元组
    2. 监听全局消息，协调子模块
    """
    def __init__(self, view: MainPageView, model: MainPageModel,
                 message_manager: MessageManager):
        super().__init__(view, model)
        self._model = model
        self._message_manager = message_manager

        # ── 组装子模块 MVP ──
        # Head
        head_model = HeadModel()
        self._head_presenter = HeadPresenter(
            view=view.head_view,
            model=head_model,
            message_manager=self._message_manager,
        )

        # DataMonitor
        data_monitor_model = DataMonitorModel()
        self._data_monitor_presenter = DataMonitorPresenter(
            view=view.data_monitor_view,
            model=data_monitor_model,
            message_manager=self._message_manager,
        )

        # ControlPanel
        control_panel_model = ControlPanelModel()
        self._control_panel_presenter = ControlPanelPresenter(
            view=view.control_panel_view,
            model=control_panel_model,
            message_manager=self._message_manager,
        )

        # 注册自身为消息处理器
        self._message_manager.register(self)

    def start(self) -> None:
        """启动后的初始化（如果有需要）"""
        pass

    def handle(self, message: Message) -> HandleResult:
        """处理连接状态消息 —— 更新 Model 并通知子模块"""
        if message.type == "serial.connection.status":
            connected = message.payload
            self._model.is_serial_connected = connected
            # ControlPanel 会通过自己的 handler 自行响应
            return HandleResult.CONTINUE
        return HandleResult.SKIP


__all__ = ["MainPagePresenter"]
