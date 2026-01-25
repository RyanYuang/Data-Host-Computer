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
        self._view.cancelBtn.clicked.connect(self.on_cancel_btn_clicked)

    def on_connect_btn_clicked(self):
        """ 处理连接按键点击事件 """
        try:
            if not self._view.port_combo:
                return
            port_name =  self._view.port_combo.getCurrentText()
            print(port_name)
            if not port_name or port_name == "未检测到串口":
                print("请选择有效的串口后再连接")
                return
           
            success = self._view.serial_manager.OpenPortByName(port_name)
            if success:
                print(f"已连接串口: {port_name}")
                # 停止刷新并关闭对话框
                self._view.refresh_timer.stop()
                self._view.accept()

            else:
                print(f"连接串口失败: {port_name}")
        except Exception as e:
            print(f"on_connect_clicked exception: {e}")

    def on_cancel_btn_clicked(self):
        """ 处理取消按键点击事件 """
        self._view.close()

    def handle(self, message: Message) -> HandleResult:
        """ 处理来自系统的其他消息"""
        return HandleResult.CONTINUE