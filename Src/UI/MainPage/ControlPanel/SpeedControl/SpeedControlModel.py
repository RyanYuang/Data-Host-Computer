from Src.MVP.base_model import BaseModel
from typing import List


class SpeedLevel:
    """速度档位"""
    def __init__(self, percentage: int = 0):
        self.percentage = percentage


class SpeedControlModel(BaseModel):
    """
    速度控制数据模型
    管理速度档位配置和当前选中状态
    """
    def __init__(self):
        super().__init__()
        self.speed_levels: List[SpeedLevel] = [
            SpeedLevel(25),
            SpeedLevel(50),
            SpeedLevel(75),
            SpeedLevel(100),
        ]
        self.current_index: int = -1  # -1 表示未选中任何档位

    def build_speed_cmd(self, btn_id: int) -> bytes:
        """根据按钮索引构建串口速度指令"""
        return f"@{btn_id + 4}\r\n".encode("ascii")
