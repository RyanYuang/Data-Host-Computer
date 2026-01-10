import PyQt6
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
import Src.Serial.SerialManger as SerialManger
from Src.UI.MainPage.MainPage import MainPage  # 修改导入方式

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # QMainWindow是PyQt6中主窗口类
    serial_manager = SerialManger.SerialManger()
    main_window = QMainWindow()
    main_page = MainPage()  # 创建MainPage实例
    main_window.setCentralWidget(main_page)  # 将MainPage设置为主窗口的中央控件
    main_window.setWindowTitle("环境监测系统")  # 设置窗口标题
    main_window.resize(1257, 1043)  # 设置窗口大小
    main_window.show()  # 显示窗口
    sys.exit(app.exec())