from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager
from Src.Serial.SerialManager import SerialManager

from .HeadModel import HeadModel
from .HeadView import HeadView

# Dialog MVP 组件
from Src.UI.Dialog.SerialConnectionDialog.SerialConnectionDialogView import SerialConnectionDialogView
from Src.UI.Dialog.SerialConnectionDialog.SerialConnectionDialogModel import SerialConnectionDialogModel
from Src.UI.Dialog.SerialConnectionDialog.SerialConnectionDialogPresenter import SerialConnectionDialogPresenter
from Src.UI.Dialog.AlertThresholdDialog.AlertThresholdView import AlertThresholdView
from Src.UI.Dialog.AlertThresholdDialog.AlertThresholdModel import AlertThresholdModel
from Src.UI.Dialog.AlertThresholdDialog.AlertThresholdPresenter import AlertThresholdPresenter


class HeadPresenter(BasePresenter, MessageHandler):
    """
    Head Presenter
    职责：
    1. 响应 View 的按钮信号
    2. 打开对话框（连接、告警设置）
    3. 监听消息更新 Model 和 View
    """
    def __init__(self, view: HeadView, model: HeadModel,
                 message_manager: MessageManager):
        super().__init__(view, model)
        self._model = model
        self._message_manager = message_manager
        self._serial_manager = SerialManager()

        # 注册消息
        self._message_manager.register(self)

        # 连接 View 信号
        self._view.connect_btn_clicked.connect(self._on_connect_clicked)
        self._view.alarm_btn_clicked.connect(self._on_alarm_clicked)
        self._view.setting_btn_clicked.connect(self._on_setting_clicked)

    # ── 用户交互处理 ──
    def _on_connect_clicked(self):
        """连接按钮：已连接时断开，未连接时打开对话框"""
        if self._model.connection_status:
            # 断开连接
            self._serial_manager.ClosePort()
            self._model.connection_status = False
            self._view.update_connection_status(False)
            self._message_manager.dispatch(
                Message("serial.connection.status", False)
            )
        else:
            # 打开连接对话框
            dialog_view = SerialConnectionDialogView(self._view)
            dialog_model = SerialConnectionDialogModel()
            dialog_presenter = SerialConnectionDialogPresenter(
                dialog_view, dialog_model, self._message_manager
            )
            dialog_view.exec()

            # 对话框关闭后检查状态
            if self._serial_manager.GetSerialStatus():
                self._model.connection_status = True
                self._view.update_connection_status(True)

    def _on_alarm_clicked(self, is_checked: bool):
        """告警按钮 —— 打开告警阈值设置对话框"""
        self._model.is_alarm_triggered = is_checked

        if is_checked:
            alert_dialog = AlertThresholdView(self._view)
            alert_model = AlertThresholdModel()
            AlertThresholdPresenter(alert_dialog, alert_model, self._message_manager)
            alert_dialog.exec()

            # 对话框关闭后重置按钮
            self._view.AlarmButton.setChecked(False)
            self._model.is_alarm_triggered = False

    def _on_setting_clicked(self):
        """设置按钮"""
        print("[HeadPresenter] Setting button clicked")

    # ── 消息处理 ──
    def handle(self, message: Message) -> HandleResult:
        if message.type == "serial.connection.status":
            self._model.connection_status = message.payload
            self._view.update_connection_status(message.payload)
            return HandleResult.CONTINUE

        if message.type == "serial.ports.available":
            self._model.available_ports = message.payload
            return HandleResult.CONSUMED

        return HandleResult.SKIP
