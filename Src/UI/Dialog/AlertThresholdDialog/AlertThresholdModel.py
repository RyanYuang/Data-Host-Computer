import sys
from dataclasses import dataclass, field
from typing import Dict, Any
import json
import os

@dataclass
class AlertThresholdModel:
    """
    告警阈值模型 - 存储所有环境数据的告警阈值配置
    """
    # 温度阈值 (摄氏度)
    temp_high: float = 45.0      # 过高告警阈值
    temp_low: float = -10.0      # 过低告警阈值
    
    # 湿度阈值 (百分比)
    humidity_high: float = 90.0  # 过高告警阈值
    humidity_low: float = 20.0   # 过低告警阈值
    
    # 气体阈值 (ppm)
    co_danger: float = 50.0      # 危险浓度
    co_warning: float = 30.0     # 警告浓度
    
    # 光照阈值 (lux)
    light_high: float = 10000.0  # 光照过高
    light_low: float = 0.0       # 光照过低
    
    # 声音告警开关
    sound_enabled: bool = True
    
    # 配置文件路径
    CONFIG_DIR: str = field(default="Config", repr=False)
    CONFIG_FILE: str = field(default="alert_thresholds.json", repr=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """将模型转换为字典用于保存"""
        return {
            "temperature": {
                "high": self.temp_high,
                "low": self.temp_low
            },
            "humidity": {
                "high": self.humidity_high,
                "low": self.humidity_low
            },
            "co": {
                "danger": self.co_danger,
                "warning": self.co_warning
            },
            "light": {
                "high": self.light_high,
                "low": self.light_low
            },
            "sound_enabled": self.sound_enabled
        }
    
    def load_from_file(self, base_path: str = ".") -> bool:
        """从配置文件加载"""
        config_path = os.path.join(base_path, self.CONFIG_DIR, self.CONFIG_FILE)
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 解析温度
                if "temperature" in data:
                    self.temp_high = data["temperature"].get("high", 45.0)
                    self.temp_low = data["temperature"].get("low", -10.0)
                    
                # 解析湿度
                if "humidity" in data:
                    self.humidity_high = data["humidity"].get("high", 90.0)
                    self.humidity_low = data["humidity"].get("low", 20.0)
                    
                # 解析气体
                if "co" in data:
                    self.co_danger = data["co"].get("danger", 50.0)
                    self.co_warning = data["co"].get("warning", 30.0)
                    
                # 解析光照
                if "light" in data:
                    self.light_high = data["light"].get("high", 10000.0)
                    self.light_low = data["light"].get("low", 0.0)
                    
                # 解析声音开关
                self.sound_enabled = data.get("sound_enabled", True)
                
                return True
        except Exception as e:
            print(f"加载告警配置失败: {e}")
        return False
    
    def save_to_file(self, base_path: str = ".") -> bool:
        """保存配置到文件"""
        config_dir = os.path.join(base_path, self.CONFIG_DIR)
        config_path = os.path.join(config_dir, self.CONFIG_FILE)
        
        try:
            # 创建配置目录
            os.makedirs(config_dir, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"保存告警配置失败: {e}")
            return False
    
    def check_alerts(self, temperature: float, humidity: float, 
                    co_level: float, light: float) -> Dict[str, list]:
        """
        检查所有数据是否超出阈值
        返回告警列表
        """
        alerts = []
        
        # 温度告警
        if temperature > self.temp_high:
            alerts.append({
                "type": "temperature",
                "level": "danger",
                "message": f"温度过高: {temperature:.1f}°C (阈值: {self.temp_high}°C)",
                "value": temperature,
                "threshold": self.temp_high
            })
        elif temperature < self.temp_low:
            alerts.append({
                "type": "temperature",
                "level": "danger", 
                "message": f"温度过低: {temperature:.1f}°C (阈值: {self.temp_low}°C)",
                "value": temperature,
                "threshold": self.temp_low
            })
            
        # 湿度告警
        if humidity > self.humidity_high:
            alerts.append({
                "type": "humidity",
                "level": "warning",
                "message": f"湿度过高: {humidity:.1f}% (阈值: {self.humidity_high}%)",
                "value": humidity,
                "threshold": self.humidity_high
            })
        elif humidity < self.humidity_low:
            alerts.append({
                "type": "humidity",
                "level": "warning",
                "message": f"湿度过低: {humidity:.1f}% (阈值: {self.humidity_low}%)",
                "value": humidity,
                "threshold": self.humidity_low
            })
            
        # 气体告警
        if co_level > self.co_danger:
            alerts.append({
                "type": "co",
                "level": "danger",
                "message": f"CO浓度危险: {co_level:.1f}ppm (危险阈值: {self.co_danger}ppm)",
                "value": co_level,
                "threshold": self.co_danger
            })
        elif co_level > self.co_warning:
            alerts.append({
                "type": "co",
                "level": "warning",
                "message": f"CO浓度警告: {co_level:.1f}ppm (警告阈值: {self.co_warning}ppm)",
                "value": co_level,
                "threshold": self.co_warning
            })
            
        # 光照告警
        if light > self.light_high:
            alerts.append({
                "type": "light",
                "level": "info",
                "message": f"光照过强: {light:.0f}lux (阈值: {self.light_high}lux)",
                "value": light,
                "threshold": self.light_high
            })
        elif light < self.light_low and self.light_low > 0:
            alerts.append({
                "type": "light",
                "level": "info",
                "message": f"光照过弱: {light:.0f}lux (阈值: {self.light_low}lux)",
                "value": light,
                "threshold": self.light_low
            })
            
        return {"alerts": alerts, "count": len(alerts)}


if __name__ == "__main__":
    # 测试
    model = AlertThresholdModel()
    print("默认配置:")
    print(json.dumps(model.to_dict(), indent=2))
    
    # 保存
    model.save_to_file()
    print("\n已保存配置")
    
    # 加载
    model2 = AlertThresholdModel()
    model2.load_from_file()
    print("\n加载后配置:")
    print(json.dumps(model2.to_dict(), indent=2))
