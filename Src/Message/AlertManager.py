from PyQt6.QtWidgets import QMessageBox, QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon, QAction
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager
import os
import subprocess
import platform


class AlertManager(MessageHandler):
    """
    告警管理器 - 集中处理所有告警通知
    """
    _instance = None
    
    def __new__(cls, message_manager: MessageManager = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, message_manager: MessageManager = None):
        if self._initialized:
            return
            
        self._message_manager = message_manager
        self._current_alerts = set()  # 当前活跃的告警
        self._tray_icon = None
        self._alert_count = 0
        self._sound_files = {}  # 存储声音文件路径
        self._system = platform.system()  # 获取系统类型
        
        # 初始化声音
        self._init_sounds()
        
        if self._message_manager:
            self._message_manager.register(self)
            
        self._initialized = True
    
    def _init_sounds(self):
        """初始化告警声音"""
        # 告警声音文件路径 (Resource 目录下)
        sound_dir = os.path.join(os.path.dirname(__file__), "..", "..", "Resource", "sounds")
        
        # 如果声音目录不存在
        if not os.path.exists(sound_dir):
            print(f"[AlertManager] 声音目录不存在: {sound_dir}")
            return
        
        # 尝试加载自定义声音文件
        danger_sound = os.path.join(sound_dir, "danger.wav")
        warning_sound = os.path.join(sound_dir, "warning.wav")
        
        if os.path.exists(danger_sound):
            self._sound_files["danger"] = danger_sound
            print(f"[AlertManager] 已找到危险声音文件: {danger_sound}")
        
        if os.path.exists(warning_sound):
            self._sound_files["warning"] = warning_sound
            print(f"[AlertManager] 已找到警告声音文件: {warning_sound}")
    
    def handle(self, message: Message) -> HandleResult:
        """处理告警消息"""
        if message.type == "alert.triggered":
            alert = message.payload
            alert_type = alert.get("type", "unknown")
            level = alert.get("level", "info")
            message_text = alert.get("message", "")
            
            # 添加到当前告警
            self._current_alerts.add(alert_type)
            self._alert_count += 1
            
            # 显示告警
            self._show_alert(level, message_text)
            
            # 播放告警声音
            if level in ["danger", "warning"]:
                self._play_alert_sound(level)
            
            # 更新托盘图标
            self._update_tray_icon()
            
            return HandleResult.CONSUMED
        
        elif message.type == "alert.cleared":
            # 告警清除
            alert_type = message.payload.get("type")
            if alert_type in self._current_alerts:
                self._current_alerts.discard(alert_type)
            self._update_tray_icon()
            
            return HandleResult.CONSUMED
        
        elif message.type == "alert.sound.play":
            # 播放告警声音
            level = message.payload.get("level", "warning")
            self._play_alert_sound(level)
            
            return HandleResult.CONSUMED
            
        elif message.type == "alert.sound.test":
            # 测试声音播放
            level = message.payload.get("level", "warning")
            self._play_alert_sound(level)
            return HandleResult.CONSUMED
            
        return HandleResult.SKIP
    
    def _show_alert(self, level: str, message: str):
        """显示告警通知"""
        # 根据级别设置图标
        if level == "danger":
            icon = QMessageBox.Icon.Critical
            title = "🚨 危险告警"
        elif level == "warning":
            icon = QMessageBox.Icon.Warning
            title = "⚠️ 警告"
        else:
            icon = QMessageBox.Icon.Information
            title = "ℹ️ 提示"
        
        # 使用 QMessageBox 显示
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    
    def _play_alert_sound(self, level: str):
        """播放告警声音"""
        print(f"[AlertManager] 播放 {level} 级别告警声音")
        
        # 方案1: 使用系统命令播放音频文件
        sound_file = self._sound_files.get(level)
        
        if sound_file and os.path.exists(sound_file):
            try:
                if self._system == "Darwin":  # macOS
                    subprocess.run(["afplay", sound_file], capture_output=True, timeout=5)
                    print(f"[AlertManager] ✅ 使用 afplay 播放: {sound_file}")
                    return
                elif self._system == "Linux":
                    subprocess.run(["aplay", sound_file], capture_output=True, timeout=5)
                    print(f"[AlertManager] ✅ 使用 aplay 播放: {sound_file}")
                    return
                elif self._system == "Windows":
                    import winsound
                    winsound.PlaySound(sound_file, winsound.SND_FILENAME)
                    print(f"[AlertManager] ✅ 使用 winsound 播放: {sound_file}")
                    return
            except subprocess.TimeoutExpired:
                print(f"[AlertManager] 播放超时")
            except FileNotFoundError as e:
                print(f"[AlertManager] 播放命令未找到: {e}")
            except Exception as e:
                print(f"[AlertManager] 系统播放失败: {e}")
        
        # 方案2: 使用 QApplication.beep()
        try:
            QApplication.beep()
            print("[AlertManager] ✅ 已播放系统蜂鸣声")
        except Exception as e:
            print(f"[AlertManager] 播放系统蜂鸣声失败: {e}")
    
    def play_danger_sound(self):
        """播放危险告警声音"""
        self._play_alert_sound("danger")
    
    def play_warning_sound(self):
        """播放警告告警声音"""
        self._play_alert_sound("warning")
    
    def test_sounds(self):
        """测试所有声音"""
        print("[AlertManager] 🔊 测试告警声音...")
        self.play_warning_sound()
    
    def _update_tray_icon(self):
        """更新托盘图标显示告警状态"""
        pass
    
    def get_active_alerts(self) -> list:
        """获取当前活跃告警列表"""
        return list(self._current_alerts)
    
    def get_alert_count(self) -> int:
        """获取告警总数"""
        return self._alert_count
    
    def clear_all_alerts(self):
        """清除所有告警"""
        self._current_alerts.clear()
        self._update_tray_icon()
