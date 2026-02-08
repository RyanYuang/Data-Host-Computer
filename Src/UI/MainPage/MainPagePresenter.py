from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager
from .MainPage import MainPage
from .ControlPanel.ControlPanel import ControlPanel


class MainPagePresenter(BasePresenter, MessageHandler):
    """Presenter for MainPage - 监听连接状态并通知 ControlPanel"""
    def __init__(self, view: MainPage, control_panel: ControlPanel, message_manager: MessageManager):
        super().__init__(view)
        self._view = view
        self._control_panel = control_panel
        self._message_manager = message_manager
        
        # 注册为消息处理器
        self._message_manager.register(self)

    def start(self) -> None:
        return None

    def handle(self, message: Message) -> HandleResult:
        """处理连接状态消息"""
        if message.type == "serial.connection.status":
            connected = message.payload
            print(f"[MainPagePresenter] 收到连接状态消息: {connected}")
            self._control_panel.on_serial_status_changed(connected)
            return HandleResult.CONSUMED
        return HandleResult.SKIP


__all__ = ["MainPagePresenter"]
