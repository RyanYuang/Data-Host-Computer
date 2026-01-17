from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from .HeadModel import HeadModel
from .HeadView import HeadView

class HeadPresenter(BasePresenter, MessageHandler):
    def __init__(self, view: HeadView, model: HeadModel, message_manager):
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
        self.model.is_alarm_triggered = self._view.AlarmButton.isChecked()
        print(f"Alarm button clicked, is_alarm_triggered: {self.model.is_alarm_triggered}")
        # In a real scenario, this might dispatch a message or update a service
        # self.message_manager.dispatch(Message("domain.alarm.set", self.model.is_alarm_triggered))


    def on_setting_button_clicked(self):
        print("Setting button clicked, should dispatch a message to open settings.")
        # self.message_manager.dispatch(Message("ui.settings.open"))

    def handle(self, message: Message) -> HandleResult:
        if message.type == "serial.connection.status":
            self.model.connection_status = message.payload
            self._view.set_connection_status(self.model.connection_status)
            return HandleResult.CONSUMED
        
        if message.type == "serial.ports.available":
            self.model.available_ports = message.payload
            # self._view.update_com_ports(self.model.available_ports) # This method does not exist yet
            return HandleResult.CONSUMED

        return HandleResult.SKIP
