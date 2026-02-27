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

    @staticmethod
    def _parse_obstacle_flag(raw_value) -> bool:
        """将障碍位解析为布尔值：1/非0 为 True，0 为 False。"""
        try:
            return int(raw_value) != 0
        except (ValueError, TypeError):
            return False


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

                # ── 仅处理传感器数据帧："@D1,D2,D3,D4[,Obstacle]\r\n" ──
                # 非 '@' 开头的帧（如 #OK:, #ERR: 反馈帧）由 SerialThread
                # 通过消息总线分发，DataEngine 不处理，直接跳过。
                if not decoded_str.startswith('@'):
                    continue

                content = decoded_str[1:]  # 移除 '@'

                # 控制指令帧（@0 ~ @8）不是传感器数据，跳过
                # 传感器数据至少包含一个逗号（@temp,hum,co,light[,obstacle]）
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
                    
                    # 支持 4 字段（兼容旧协议）或 5 字段（新增障碍位）
                    if len(parsed_data) in (4, 5):
                        sensor_values = parsed_data[:4]
                        obstacle_detected = False
                        if len(parsed_data) == 5:
                            obstacle_detected = self._parse_obstacle_flag(parsed_data[4])

                        self.packet_parsed.emit(sensor_values)
                        
                        # 发送传感器数据更新消息（供告警系统使用）
                        if self._message_manager:
                            sensor_data = {
                                "temperature": sensor_values[0],   # 温度
                                "humidity": sensor_values[1],      # 湿度
                                "co": sensor_values[2],            # CO浓度
                                "light": sensor_values[3],         # 光照强度
                                "obstacle": obstacle_detected,     # 障碍标志
                            }
                            self._message_manager.dispatch(
                                Message("sensor.data.updated", sensor_data)
                            )

                            # 独立发布障碍状态消息，供 UI 醒目提示
                            self._message_manager.dispatch(
                                Message("sensor.obstacle.status", {
                                    "detected": obstacle_detected
                                })
                            )
                    else:
                        print(f"[CarDataEngine] 字段数量不匹配 "
                              f"(期望 4 或 5, 实际 {len(parsed_data)}): '{decoded_str}'")

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
