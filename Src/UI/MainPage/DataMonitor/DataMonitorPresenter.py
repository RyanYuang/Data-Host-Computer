from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from .DataMonitorModel import DataMonitorModel
from .DataMonitorView import DataMonitorView
from Src.DataEngine.CarDataEngine import CarDataEngine


class DataMonitorPresenter(BasePresenter, MessageHandler):
    def __init__(self, view: DataMonitorView, model: DataMonitorModel, message_manager):
        # The BasePresenter's __init__ is not called because we need to
        # manually set the presenter on the view, and it doesn't do anything else.
        # super().__init__(view) 
        self._view = view
        self._view.presenter = self
        
        self._model = model
        self._message_manager = message_manager
        
        # Register to handle messages if a message manager is provided
        if self._message_manager:
            self._message_manager.register(self)

        CarDataEngineInstance = CarDataEngine()
        CarDataEngineInstance.bind_slot(self.refresh_all_values)
        
        self.init_view()

    def init_view(self):
        """
        Initializes the view with data from the model.
        """
        initial_data = self._model.get_all_data()
        self._view.init_ui(initial_data)

    def refresh_all_values(self, datapack):
        """
        Refreshes all values in the view with current data from the model.
        仅接受包含 4 个数值的列表，其他类型一律忽略。
        """
        # 防御性校验：必须是 list 且长度 == 4
        if not isinstance(datapack, list) or len(datapack) != 4:
            return

        for i in range(len(datapack)):
            self._view.update_value_at(i, datapack[i])


    def handle(self, message: Message) -> HandleResult:
        """
        Handles messages from the MessageManager.
        This is where you would react to messages that should update the data monitor.
        
        For example, a message might contain new sensor data.
        """
        # 处理传感器告警状态消息
        if message.type == "sensor.alert.status":
            alert_types = message.payload.get("alert_types", [])
            
            # 数据类型到索引的映射（对应温度、湿度、CO、光照）
            type_to_index = {
                "temperature": 0,
                "humidity": 1,
                "co": 2,
                "light": 3
            }
            
            # 首先停止所有闪烁
            self._view.stop_all_blink()
            
            # 对于超阈值的数据，开始闪烁
            for alert_type in alert_types:
                if alert_type in type_to_index:
                    index = type_to_index[alert_type]
                    self._view.start_blink(index)
            
            return HandleResult.CONTINUE
        
        # 不处理其他消息，继续传递
        return HandleResult.CONTINUE
