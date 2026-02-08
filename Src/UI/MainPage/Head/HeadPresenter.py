from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager
from .HeadModel import HeadModel
from .HeadView import HeadView
from Src.UI.Dialog.AlertThresholdDialog.AlertThresholdView import AlertThresholdView
from Src.UI.Dialog.AlertThresholdDialog.AlertThresholdModel import AlertThresholdModel
from Src.UI.Dialog.AlertThresholdDialog.AlertThresholdPresenter import AlertThresholdPresenter

class HeadPresenter(BasePresenter, MessageHandler):
    def __init__(self, view: HeadView, model: HeadModel, message_manager: MessageManager):
        super().__init__(view)
        self.model = model
        self.message_manager = message_manager
        self.message_manager.register(self)
        self._view = view

        self._view.ConnectButton.clicked.connect(self.on_connect_button_clicked)
        self._view.AlarmButton.clicked.connect(self.on_alarm_button_clicked)
        self._view.SettingButton.clicked.connect(self.on_setting_button_clicked)

    def on_connect_button_clicked(self):
        # This would dispatch a message to open the connection dialog
        # For now, we will just print a message
        print("Connect button clicked, should dispatch a message.")
        # In a real scenario:
        # self.message_manager.dispatch(Message("ui.head.connect_clicked"))

    def on_alarm_button_clicked(self):
        """告警按钮点击 - 打开告警设置对话框"""
        self.model.is_alarm_triggered = self._view.AlarmButton.isChecked()
        
        if self.model.is_alarm_triggered:
            # 点击后打开告警设置对话框
            alert_dialog = AlertThresholdView(self._view)
            alert_model = AlertThresholdModel()
            alert_presenter = AlertThresholdPresenter(alert_dialog, alert_model, self.message_manager)
            alert_dialog.exec()
            
            # 对话框关闭后，重置按钮状态（因为对话框是用来设置的，不是触发的）
            self._view.AlarmButton.setChecked(False)
            self.model.is_alarm_triggered = False
        else:
            print(f"Alarm button unchecked, is_alarm_triggered: {self.model.is_alarm_triggered}")


    def on_setting_button_clicked(self):
        print("Setting button clicked, should dispatch a message to open settings.")
        # self.message_manager.dispatch(Message("ui.settings.open"))

    def handle(self, message: Message) -> HandleResult:
        if message.type == "serial.connection.status":
            self.model.connection_status = message.payload
            # self._view.set_connection_status(self.model.connection_status)
            return HandleResult.CONTINUE
        
        if message.type == "serial.ports.available":
            self.model.available_ports = message.payload
            # self._view.update_com_ports(self.model.available_ports) # This method does not exist yet
            return HandleResult.CONSUMED

        return HandleResult.SKIP
