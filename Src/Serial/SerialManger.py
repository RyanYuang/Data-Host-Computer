import serial
import serial.tools.list_ports

class SerialManger:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SerialManger, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if self._initialized:
            return
        
        self.serial = serial.Serial()
        self.serial.baudrate = 115200
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 0.1  # Set a short timeout for read operations
        self._initialized = True

    def GetSerialList(self):
        """
        @brief 获取串口列表
        :return: 串口信息对象的列表
        """
        return serial.tools.list_ports.comports()

    def GetSerialStatus(self):
        """
        @brief 获取串口状态
        :return: 串口状态
        """
        return self.serial.is_open

    def OpenPortByName(self, port_name: str, baudrate: int = 115200) -> bool:
        """按名称打开串口，返回是否成功。"""
        if self.serial.is_open:
            self.ClosePort()
        
        try:
            self.serial.port = port_name
            self.serial.baudrate = baudrate
            self.serial.open()
            return True
        except serial.SerialException as e:
            print(f"OpenPortByName: failed to open {port_name}: {e}")
            return False

    def ClosePort(self) -> None:
        """关闭当前串口（如果已打开）。"""
        if self.serial.is_open:
            try:
                self.serial.close()
            except Exception as e:
                print(f"ClosePort exception: {e}")
    
    def read(self, num_bytes: int):
        """Reads data from the serial port."""
        if not self.serial.is_open:
            return None
        try:
            return self.serial.read(num_bytes)
        except serial.SerialException as e:
            print(f"Serial read error: {e}")
            self.ClosePort()
            return None

    def read_all(self):
        """Read all available bytes from serial buffer."""
        if not self.serial.is_open:
            return None
        try:
            # in_waiting gets the number of bytes in the input buffer
            if self.serial.in_waiting > 0:
                return self.serial.read(self.serial.in_waiting)
            return None
        except serial.SerialException as e:
            print(f"Serial read_all error: {e}")
            self.ClosePort()
            return None

    def write(self, data: bytes):
        """Writes data to the serial port."""
        if not self.serial.is_open:
            return False
        try:
            self.serial.write(data)
            return True
        except serial.SerialException as e:
            print(f"Serial write error: {e}")
            self.ClosePort()
            return False
        
    

