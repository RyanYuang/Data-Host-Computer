import PyQt6.QtSerialPort as QTSerial
from PyQt6 import QtCore
import SerialManger as SerialManger


class SerialThread(QTSerial.QSerialPort):
    data_received = QtCore.pyqtSignal(bytes)

    def __init__(self, parent=None):
        QTSerial.QSerialPort.__init__(self, parent)
        self.serial_manager = SerialManger.SerialManger()
        self._paused = False
        self._running = False

    # 线程启动函数
    def start(self) -> bool:
        """打开串口并开始监听 readyRead 信号。

        如果没有指定端口，会尝试使用第一个可用端口。
        返回 True 表示成功打开，False 表示失败或没有可用端口。
        """
        if self.serial_manager.isOpen():
            self._running = True
            return True

        ports = self.serial_manager.GetSerialList()
        if not ports:
            print("SerialThread.start: no serial ports available")
            return False

        port_info = ports[0]
        try:
            self.serial_manager.setPort(port_info)
            opened = self.serial_manager.open(QTSerial.QSerialPort.OpenModeFlag.ReadWrite)
            if not opened:
                print(f"SerialThread.start: failed to open port {port_info.portName()}")
                return False

            # 连接数据就绪信号
            try:
                self.serial_manager.readyRead.connect(self._on_ready_read)
            except Exception:
                # ignore if already connected or connection fails
                pass

            self._running = True
            self._paused = False
            return True
        except Exception as e:
            print(f"SerialThread.start: exception opening port: {e}")
            return False

    # 线程停止函数
    def stop(self) -> None:
        """停止监听并关闭串口。"""
        self._running = False
        self._paused = False
        try:
            try:
                self.serial_manager.readyRead.disconnect(self._on_ready_read)
            except Exception:
                pass
            if self.serial_manager.isOpen():
                self.serial_manager.close()
        except Exception as e:
            print(f"SerialThread.stop: exception: {e}")

    # 线程挂起函数
    def pause(self) -> None:
        """暂停接收数据（会在 readyRead 回调中忽略数据）。"""
        self._paused = True

    # 线程恢复函数
    def resume(self) -> None:
        """恢复接收数据。"""
        self._paused = False

    # 线程运行函数
    def run(self) -> None:
        """兼容性的运行入口：尝试启动串口监听。

        注意：此类不是 QThread 子类，run 只是便捷入口，不会创建新线程。
        """
        return self.start()

    def _on_ready_read(self) -> None:
        """内部 readyRead 处理器，将读取到的数据以 bytes 形式通过 `data_received` 发出。"""
        if not self._running or self._paused:
            # 如果暂停或已停止，直接丢弃数据
            try:
                _ = self.serial_manager.readAll()
            except Exception:
                pass
            return

        try:
            qba = self.serial_manager.readAll()
            # QByteArray -> bytes
            data = bytes(qba)
            if data:
                self.data_received.emit(data)
        except Exception as e:
            print(f"SerialThread._on_ready_read: read error: {e}")

