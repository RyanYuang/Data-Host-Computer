from Src.MVP.base_model import BaseModel
from typing import List
from datetime import datetime


class SerialConsoleModel(BaseModel):
    """
    串口控制台数据模型
    管理原始串口收发数据的日志记录
    """
    # 最大保留条数，防止内存溢出
    MAX_LOG_LINES = 2000

    def __init__(self):
        super().__init__()
        self._logs: List[str] = []
        self.auto_scroll: bool = True
        self.show_timestamp: bool = True

    @property
    def logs(self) -> List[str]:
        return self._logs

    def append(self, direction: str, raw_text: str) -> str:
        """
        追加一条日志。

        :param direction: "RX" 或 "TX"
        :param raw_text:  原始文本（已 strip）
        :return: 格式化后的行文本
        """
        if self.show_timestamp:
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            line = f"[{ts}] {direction} │ {raw_text}"
        else:
            line = f"{direction} │ {raw_text}"

        self._logs.append(line)

        # 超出上限时裁剪前面的旧记录
        if len(self._logs) > self.MAX_LOG_LINES:
            self._logs = self._logs[-self.MAX_LOG_LINES:]

        return line

    def clear(self):
        """清空所有日志"""
        self._logs.clear()

    @property
    def line_count(self) -> int:
        return len(self._logs)
