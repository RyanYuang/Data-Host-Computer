from Src.MVP.base_presenter import BasePresenter
from .DirectionControlPanelModel import DirectionControlPanelModel
from .DirectionControlPanelView import DirectionControlPanelView
from Src.Serial.SerialManager import SerialManager


class DirectionControlPanelPresenter(BasePresenter):
    def __init__(self, view: DirectionControlPanelView, model: DirectionControlPanelModel, message_manager=None):
        super().__init__(view, model)
        self.serial = SerialManager()

    def left_btn_clicked(self):
        print("Left button clicked")
        data_pack = b'@3\r\n'
        self.serial.write(data_pack)

    def right_btn_clicked(self):
        print("Right button clicked")
        data_pack = b'@4\r\n'
        self.serial.write(data_pack)

    def up_btn_clicked(self):
        print("Up button clicked")
        data_pack = b'@1\r\n'
        self.serial.write(data_pack)

    def down_btn_clicked(self):
        print("Down button clicked")
        data_pack = b'@2\r\n'
        self.serial.write(data_pack)

    def mid_btn_clicked(self):
        print("Stop button clicked")
        data_pack = b'@0\r\n'
        self.serial.write(data_pack)
