from PyQt6.QtCore import QObject, pyqtSignal, QThread
from .SerialManger import SerialManger
import time
from Src.DataEngine.DataEngineBase import DataEngine


class SerialThread(QThread):
    data_received = pyqtSignal(bytes)

    def __init__(self, parent=None, name=None):
        super().__init__(parent)
        self.serial_manager = SerialManger()
        self._running = False
        self.name = name

    def run(self):
        """线程运行函数，循环读取串口数据。"""
        self._running = True
        print("串口线程已启动...")
        while self._running:
            if self.serial_manager.GetSerialStatus():
                # 串口已打开
                try:
                    data = self.serial_manager.read_all()
                    if data:
                        # print(data.decode('utf-8',errors='ignore'),end='')
                        self.data_received.emit(data)
                    # else:
                    #     # 可以在这里取消注释来查看持续轮询的状态
                    #     print("串口线程: 串口已连接，但无数据")
                except Exception as e:
                    print(f"SerialThread.run: read error: {e}")
                    time.sleep(0.1)
            else:
                # 串口未打开
                print("串口线程: 等待串口连接...")
                # 如果串口未连接，则休眠较长时间以减少打印输出
                time.sleep(1)
            
            # 短暂休眠，避免忙等待
            self.msleep(20) # 20ms

    def stop(self) -> None:
        """停止线程。"""
        self._running = False
        # 等待线程安全退出
        self.wait()
    
    def BindDataEngine(self, data_engine:DataEngine):
        print("绑定数据引擎")
        self.data_received.connect(data_engine.push_data)

