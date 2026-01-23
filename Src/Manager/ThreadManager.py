from PyQt6.QtCore import QObject, QThread
from typing import Dict, Optional, Callable

class ThreadManager(QObject):
    """
    线程管理器 (Singleton)
    用于管理应用程序中的工作线程 (QThread) 及其对应的工作对象 (Worker)。
    
    功能：
    1. 启动线程：将 Worker 对象移入新线程并启动。
    2. 停止线程：安全退出线程并清理资源。
    3. 全局管理：记录所有活跃线程，支持一键停止所有线程（用于程序退出时）。
    """
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ThreadManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if ThreadManager._is_initialized:
            return
        super().__init__()
        # 存储线程对象: {name: QThread}
        self._threads: Dict[str, QThread] = {}
        # 存储工作对象: {name: QObject}
        self._workers: Dict[str, QObject] = {}
        ThreadManager._is_initialized = True
    # def add_worker(self, name: str, worker: QObject):
        
    def start_worker(self, name: str, worker: QObject, start_slot: Optional[Callable] = None):
        """
        将 worker 移入新线程并启动。

        :param name: 线程/任务的唯一标识名称 (例如 "DataEngine", "SerialPort")
        :param worker: 业务逻辑对象 (必须继承自 QObject)
        :param start_slot: (可选) 线程启动后立即执行的函数 (通常是 worker 的某个方法)
        """
        if name in self._threads:
            print(f"[ThreadManager] Warning: Thread '{name}' is already running.")
            return

        # 1. 创建线程
        thread = QThread()
        
        # 2. 将 worker 移动到该线程
        worker.moveToThread(thread)
        
        # 3. 缓存引用，防止对象被垃圾回收
        self._threads[name] = thread
        self._workers[name] = worker
        
        # 4. 如果提供了启动槽函数，连接到 thread.started 信号
        print(f"[ThreadManager] Starting thread '{name}'...")
        if start_slot:
            thread.started.connect(start_slot)
        # 5. 设置清理逻辑：线程结束时自动清理字典
        thread.finished.connect(lambda: self._cleanup(name))
        
        # 6. 启动线程
        thread.start()
        print(f"[ThreadManager] Thread '{name}' started.")

    def stop_worker(self, name: str):
        """
        停止指定名称的线程。
        """
        if name in self._threads:
            thread = self._threads[name]
            if thread.isRunning():
                thread.quit()
                thread.wait() # 阻塞等待线程结束
            # _cleanup 会通过 finished 信号被调用
        else:
            print(f"[ThreadManager] Thread '{name}' not found or already stopped.")

    def stop_all(self):
        """停止所有受管理的线程。通常在程序关闭时调用。"""
        print("[ThreadManager] Stopping all threads...")
        for name in list(self._threads.keys()):
            self.stop_worker(name)

    def _cleanup(self, name: str):
        """内部清理资源"""
        if name in self._threads: del self._threads[name]
        if name in self._workers: del self._workers[name]
        print(f"[ThreadManager] Resources for '{name}' cleaned up.")