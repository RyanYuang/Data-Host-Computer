from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager

from .SerialConsoleModel import SerialConsoleModel
from .SerialConsoleView import SerialConsoleView


class SerialConsolePresenter(BasePresenter, MessageHandler):
    """
    串口控制台 Presenter
    职责：
    1. 监听 serial.data.raw（下位机→上位机）和 serial.data.tx（上位机→下位机）消息
    2. 写入 Model，更新 View
    3. 响应用户操作（清空、开关时间戳等）
    """
    def __init__(self, view: SerialConsoleView, model: SerialConsoleModel,
                 message_manager: MessageManager):
        super().__init__(view, model)
        self._model = model
        self._message_manager = message_manager

        # 注册消息处理
        self._message_manager.register(self)

        # 连接 View 信号
        self._view.clear_clicked.connect(self._on_clear)
        self._view.auto_scroll_toggled.connect(self._on_auto_scroll)
        self._view.timestamp_toggled.connect(self._on_timestamp)

    # ── 消息处理 ──
    def handle(self, message: Message) -> HandleResult:
        # 接收到下位机原始数据
        if message.type == "serial.data.raw":
            raw = message.payload.get("data", "")
            if raw:
                line = self._model.append("RX", raw)
                self._view.append_line(line, "RX")
                self._view.update_line_count(self._model.line_count)
            return HandleResult.CONTINUE  # 不消费，让其他 handler 也能处理

        # 上位机发送的指令（可选：由发送侧 dispatch）
        if message.type == "serial.data.tx":
            raw = message.payload.get("data", "")
            if raw:
                line = self._model.append("TX", raw)
                self._view.append_line(line, "TX")
                self._view.update_line_count(self._model.line_count)
            return HandleResult.CONTINUE

        return HandleResult.SKIP

    # ── 用户操作 ──
    def _on_clear(self):
        """清空日志"""
        self._model.clear()
        self._view.clear_console()
        self._view.update_line_count(0)

    def _on_auto_scroll(self, enabled: bool):
        """切换自动滚动"""
        self._model.auto_scroll = enabled

    def _on_timestamp(self, enabled: bool):
        """切换时间戳显示"""
        self._model.show_timestamp = enabled
