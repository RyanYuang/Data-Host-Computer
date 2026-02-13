from Src.MVP.base_model import BaseModel


class MainPageModel(BaseModel):
    """
    MainPage 的数据模型
    管理主页面的状态数据
    """
    def __init__(self):
        super().__init__()
        self.is_serial_connected: bool = False
        self.window_title: str = "环境监测控制系统"
