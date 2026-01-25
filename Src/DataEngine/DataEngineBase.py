from PyQt6.QtCore import QObject, pyqtSignal

class DataEngine(QObject):
    """
    数据解析引擎基类 (Base Class for Data Parsing Engine)
    
    功能：
    1. 缓存串口接收到的字节流。
    2. 提供解析接口供子类实现具体协议。
    3. 通过信号发送解析后的数据。
    """
    
    # 信号：当成功解析出一个完整数据包时发出
    # data: 解析后的数据，类型由子类决定（如 dict, str, 自定义对象等）
    packet_parsed = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 内部接收缓冲区
        self._buffer = bytearray()

    def push_data(self, data: bytes):
        """
        接收原始数据并存入缓冲区，随后尝试解析。
        通常连接到串口线程的 data_received 信号。
        :param data: 串口接收到的字节数据
        """
        if not data:
            return
        self._buffer.extend(data)
        self.process_buffer()

    def process_buffer(self):
        """
        处理缓冲区的虚函数。
        子类必须重写此方法以实现特定的协议解析逻辑。
        
        在子类实现建议：
        1. 循环检查 self._buffer 是否包含完整的数据包（检查帧头、帧尾、长度等）。
        2. 如果有，提取并处理，发射 packet_parsed 信号。
        3. 从 self._buffer 中移除已处理的字节 (del self._buffer[0:pkg_len])。
        4. 如果数据不足或不完整，保留在缓冲区等待下一次数据到来。
        """
        raise NotImplementedError("DataEngine 子类必须实现 process_buffer 方法")

    def clear(self):
        """清空缓冲区"""
        self._buffer.clear()
        
    def get_buffer_size(self) -> int:
        """获取当前缓冲区大小"""
        return len(self._buffer)
    
    def bind_slot(self, slot:QObject):
        self.packet_parsed.connect(slot)

    def unbind_slot(self, slot:QObject):
        self.packet_parsed.disconnect(slot)