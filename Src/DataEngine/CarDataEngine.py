def singleton(class_):
    """
    A decorator to turn a class into a singleton.
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance

from Src.DataEngine.DataEngineBase import DataEngine
from Src.Message.MessageManager import MessageManager
from Src.Message.Message import Message

@singleton
class CarDataEngine(DataEngine):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._message_manager = None  # 消息管理器引用

    def set_message_manager(self, message_manager: MessageManager):
        """设置消息管理器"""
        self._message_manager = message_manager


    def process_buffer(self):
        while True:
            try:
                # 查找换行符索引
                index = self._buffer.index(b'\n')
                # 提取完整的一行数据（包含换行符）
                packet_bytes = self._buffer[:index+1]
                # 从缓冲区移除这部分数据
                del self._buffer[:index+1]
                
                # 解析逻辑
                decoded_str = packet_bytes.decode('utf-8').strip()

                # ── 仅处理传感器数据帧："@D1,D2,D3,D4\r\n" ──
                # 非 '@' 开头的帧（如 #OK:, #ERR: 反馈帧）由 SerialThread
                # 通过消息总线分发，DataEngine 不处理，直接跳过。
                if not decoded_str.startswith('@'):
                    continue

                content = decoded_str[1:]  # 移除 '@'

                # 控制指令帧（@0 ~ @8）不是传感器数据，跳过
                # 传感器数据至少包含一个逗号（@temp,hum,co,light）
                if ',' not in content:
                    continue

                parts = content.split(',')
                
                parsed_data = []
                try:
                    for part in parts:
                        num_str = part.strip()
                        if not num_str:
                            continue  # 忽略由,,或尾随,引起的空部分
                        
                        # 同时支持整形和浮点型
                        if '.' in num_str:
                            parsed_data.append(float(num_str))
                        else:
                            parsed_data.append(int(num_str))
                    
                    # 仅在成功解析出 4 个字段时视为有效传感器数据
                    if len(parsed_data) == 4:
                        self.packet_parsed.emit(parsed_data)
                        
                        # 发送传感器数据更新消息（供告警系统使用）
                        if self._message_manager:
                            sensor_data = {
                                "temperature": parsed_data[0],  # 温度
                                "humidity": parsed_data[1],     # 湿度
                                "co": parsed_data[2],           # CO浓度
                                "light": parsed_data[3],        # 光照强度
                            }
                            self._message_manager.dispatch(
                                Message("sensor.data.updated", sensor_data)
                            )
                    else:
                        print(f"[CarDataEngine] 字段数量不匹配 "
                              f"(期望 4, 实际 {len(parsed_data)}): '{decoded_str}'")

                except ValueError as e:
                    print(f"[CarDataEngine] 数值解析错误: {e}, 原始帧: '{decoded_str}'")
                
            except ValueError:
                # 缓冲区中没有找到 \n，等待更多数据
                break
            except Exception as e:
                print(f"Parsing error: {e}")
                # 发生错误时可能需要清理缓冲区以防死循环
                self.clear()
                break
