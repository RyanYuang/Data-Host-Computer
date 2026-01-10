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
        return serialList
    def GetSerialStatus(self):
        """
        @brief 获取串口状态
        :return: 串口状态
        """
        print("GetSerialStatus")
        return self.isOpen()
    

