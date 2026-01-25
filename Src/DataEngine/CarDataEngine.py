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

@singleton
class CarDataEngine(DataEngine):
    def __init__(self, parent=None):
        super().__init__(parent)


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

                # 数据包格式: "@D1,D2,D3,D4,D5\r\n"
                if decoded_str.startswith('@'):
                    content = decoded_str[1:]  # 移除 '@'
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
                        
                        # 仅在成功解析出数据时发送列表
                        if parsed_data:
                            self.packet_parsed.emit(parsed_data)

                    except ValueError as e:
                        print(f"Parsing data error: {e}, packet: '{decoded_str}'")
                        # 发生转换错误时，发送原始字符串以供调试
                        self.packet_parsed.emit(decoded_str)
                
                else:
                    # 对于不符合格式的数据包，发送原始字符串
                    self.packet_parsed.emit(decoded_str)
                
            except ValueError:
                # 缓冲区中没有找到 \n，等待更多数据
                break
            except Exception as e:
                print(f"Parsing error: {e}")
                # 发生错误时可能需要清理缓冲区以防死循环
                self.clear()
                break
