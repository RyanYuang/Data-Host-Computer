from Src.MVP.base_presenter import BasePresenter
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from .SerialConnectionDialogModel import SerialConnectionDialogModel
from .SerialConnectionDialogView import SeireConnectionDialogView

class SerialConnectionDialogPresenter(BasePresenter,MessageHandler):
    def __init__(self, view: SeireConnectionDialogView, model: SerialConnectionDialogModel,message_manager):
        super().__init__(view)
        self.model = model
        self.message = message_manager

        # 注册为消息处理器
        self.message.register(self)

        # 注册控件回调函数
        self._view.confirmBtn.clicked.connect(self.on_connect_btn_clicked)



    def on_connect_btn_clicked(self):
        """ 处理连接按键点击事件 """
        print("on_connect_btn_clicked")