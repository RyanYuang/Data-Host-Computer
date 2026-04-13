import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from Src.Startup.StartupManager import run_startup
from Src.Manager.ThreadManager import ThreadManager
from Src.Serial.SerialThread import SerialThread
from Src.DataEngine.CarDataEngine import CarDataEngine
from Src.Message.MessageManager import MessageManager
from Src.Message.AlertManager import AlertManager

# MVP
from Src.UI.MainPage.MainPage import MainPageView
from Src.UI.MainPage.MainPageModel import MainPageModel
from Src.UI.MainPage.MainPagePresenter import MainPagePresenter


if __name__ == "__main__":
    # ── 启动前检查（如 --serial-test） ──
    exit_code = run_startup(sys.argv)
    if exit_code is not None:
        sys.exit(exit_code)

    app = QApplication(sys.argv)

    # ── 基础设施层 ──
    message_manager = MessageManager()
    data_engine = CarDataEngine()
    data_engine.set_message_manager(message_manager)

    # ── 线程管理 ──
    thread_manager = ThreadManager()
    serial_thread = SerialThread(name="SerialThread-1")
    serial_thread.set_message_manager(message_manager)
    serial_thread.BindDataEngine(data_engine)
    thread_manager.start_worker("serial_thread", serial_thread, serial_thread.start)

    # ── 告警管理器 ──
    alert_manager = AlertManager(message_manager)

    # # ── 主界面 MVP 组装 ──
    main_window = QMainWindow()
    main_view = MainPageView()
    main_model = MainPageModel()
    main_presenter = MainPagePresenter(
        view=main_view,
        model=main_model,
        message_manager=message_manager,
    )
    main_view.presenter = main_presenter  # 设置 presenter 引用以支持键盘快捷键
    main_presenter.start()

    main_window.setCentralWidget(main_view)
    main_window.setWindowTitle("环境监测系统")
    main_window.resize(1257, 818)
    main_window.show()

    # ── 应用退出时清理资源 ──
    app.aboutToQuit.connect(alert_manager.cleanup)

    sys.exit(app.exec())