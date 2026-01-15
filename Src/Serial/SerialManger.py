import PyQt6.QtSerialPort as QTSerial

class SerialManger(QTSerial.QSerialPort):
    def __init__(self, parent=None):
        QTSerial.QSerialPort.__init__(self, parent)
        # 默认配置
        """
            baud rate   9600
            StopBits    1
            DataBIts    8
            Parity      None
            Flowctl     None
        """
        # 写死配置
        self.setStopBits(self.stopBits().OneStop) #1 bit
        self.setDataBits(self.dataBits().Data8)
        self.setParity(self.parity().NoParity)
        self.setFlowControl(self.flowControl().NoFlowControl)
        self.setBaudRate(9600)

    # 获取函数
    def GetSerialInfo(self):
        """
        @brief 获取串口信息
        :return: 串口信息
        """
        print("GetSerialInfo")
        return
    def GetSerialList(self):
        """
        @brief 获取串口列表
        :return: 串口列表
        """
        print("GetSerialList")
        serialList = QTSerial.QSerialPortInfo.availablePorts()
        print(f"serialList: {serialList}")
        return serialList
    def GetSerialStatus(self):
        """
        @brief 获取串口状态
        :return: 串口状态
        """
        print("GetSerialStatus")
        return self.isOpen()
    
    def OpenPortByName(self, port_name: str) -> bool:
        """按名称打开串口，返回是否成功。"""
        try:
            ports = QTSerial.QSerialPortInfo.availablePorts()
            target = None
            for p in ports:
                if p.portName() == port_name:
                    target = p
                    break
            if target is None:
                print(f"OpenPortByName: port {port_name} not found")
                return False

            self.setPort(target)
            opened = self.open(QTSerial.QSerialPort.OpenModeFlag.ReadWrite)
            if not opened:
                print(f"OpenPortByName: failed to open {port_name}")
                return False
            return True
        except Exception as e:
            print(f"OpenPortByName exception: {e}")
            return False

    def ClosePort(self) -> None:
        """关闭当前串口（如果已打开）。"""
        try:
            if self.isOpen():
                self.close()
        except Exception as e:
            print(f"ClosePort exception: {e}")
        
    

