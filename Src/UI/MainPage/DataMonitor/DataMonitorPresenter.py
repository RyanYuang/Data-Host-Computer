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
        """
        for i in range(len(datapack)):
            self._view.update_value_at(i, datapack[i])


    def handle(self, message: Message) -> HandleResult:
        """
        Handles messages from the MessageManager.
        This is where you would react to messages that should update the data monitor.
        
        For example, a message might contain new sensor data.
        """
        # Example:
        # if message.type == "SENSOR_DATA_UPDATE":
        #     data = message.data 
        #     # find index for data.name
        #     # self.update_single_value(index, data.value)
        #     return HandleResult.HANDLED

        # By default, continue processing
        return HandleResult.CONTINUE
