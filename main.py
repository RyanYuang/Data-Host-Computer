import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Src.Startup.StartupManager import run_startup
from Src.UI.MainPage.MainPage import MainPage  # 修改导入方式
from Src.UI.MainPage.MainPagePresenter import MainPagePresenter
from Src.Manager.ThreadManager import ThreadManager
from Src.Serial.SerialThread import SerialThread
from Src.Serial.SerialManger import SerialManger
from Src.DataEngine.CarDataEngine import CarDataEngine

if __name__ == "__main__":
    exit_code = run_startup(sys.argv)
    if exit_code is not None:
        sys.exit(exit_code)
    app = QApplication(sys.argv)
    # 创建数据引擎
    data_engine = CarDataEngine()

    # 创建线程管理器
    thread_manager = ThreadManager()
    # 创建串口线程
    serial_thread = SerialThread(name="SerialThread-1")
    thread_manager.start_worker("serial_thread", serial_thread, serial_thread.start)
    serial_thread.BindDataEngine(data_engine)


    # QMainWindow是PyQt6中主窗口类
    main_window = QMainWindow()
    main_page = MainPage()  # 创建MainPage实例
    # 将 MainPage 与 Presenter 绑定（MVP）
    presenter = MainPagePresenter(main_page)
    presenter.start()
    main_window.setCentralWidget(main_page)  # 将MainPage设置为主窗口的中央控件
    main_window.setWindowTitle("环境监测系统")  # 设置窗口标题
    main_window.resize(1257, 818)  # 设置窗口大小
    main_window.show()  # 显示窗口
    sys.exit(app.exec())