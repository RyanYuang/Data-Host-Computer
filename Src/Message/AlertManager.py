from PyQt6.QtWidgets import QMessageBox, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon, QAction
from Src.Message.MessageHandler import MessageHandler
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageManager import MessageManager


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
        
        if self._message_manager:
            self._message_manager.register(self)
            
        self._initialized = True
    
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
        
        # 使用 QMessageBox 显示（会阻塞，但告警需要用户注意）
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    
    def _play_alert_sound(self, level: str):
        """播放告警声音"""
        # TODO: 实现声音播放
        # 可以使用 QSound 或系统 API
        print(f"🔔 播放告警声音: {level}")
    
    def _update_tray_icon(self):
        """更新托盘图标显示告警状态"""
        # TODO: 实现系统托盘图标
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
