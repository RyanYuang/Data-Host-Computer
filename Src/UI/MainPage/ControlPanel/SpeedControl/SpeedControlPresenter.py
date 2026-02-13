from Src.MVP.base_presenter import BasePresenter
from Src.Serial.SerialManager import SerialManager
from .SpeedControlModel import SpeedControlModel
from .SpeedControlView import SpeedControlView


class SpeedControlPresenter(BasePresenter):
    """
    速度控制 Presenter
    职责：根据 Model 初始化 View，处理用户点击并发送串口指令
    """
    def __init__(self, view: SpeedControlView, model: SpeedControlModel):
        super().__init__(view, model)
        self._model = model
        self._serial = SerialManager()

        # 用 Model 数据初始化 View 的按钮文本
        labels = [f"{lvl.percentage}%" for lvl in self._model.speed_levels]
        self._view.init_speed_buttons(labels)

        # 监听 View 的按钮点击信号
        self._view.speed_btn_clicked.connect(self._on_speed_selected)

    def _on_speed_selected(self, btn_id: int):
        """用户选择速度档位"""
        self._model.current_index = btn_id
        data_pack = self._model.build_speed_cmd(btn_id)
        self._serial.write(data_pack)
