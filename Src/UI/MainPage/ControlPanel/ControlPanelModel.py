from Src.MVP.base_model import BaseModel


class ControlPanelModel(BaseModel):
    """
    控制面板数据模型
    管理控制面板的状态
    """
    def __init__(self):
        super().__init__()
        self.is_serial_connected: bool = False
