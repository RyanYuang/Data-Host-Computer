from Src.MVP.base_model import BaseModel
from Src.DataEngine.CarDataEngine import CarDataEngine

# 定义数据项结构体类
class DataItem:
    def __init__(self, icon_path, name, data_value):
        self.icon_path = icon_path  # 图标路径
        self.name = name            # 数据名称
        self.data_value = data_value  # 实际数据值

        

class DataMonitorModel(BaseModel):
    """
    用于存储 DataMonitor 视图状态的数据模型。
    """
    def __init__(self):
        super().__init__()
        self.data_array = []

        # 初始化数据
        self._init_data()
        

    def _init_data(self):
        """初始化数据数组"""
        self.data_array.clear()
        self.data_array.append(DataItem("Resource/Tempreture.png", "温度", 25.6))
        self.data_array.append(DataItem("Resource/Humidity.png", "湿度", 60.3))
        self.data_array.append(DataItem("Resource/CO.png", "一氧化碳", 0.5))
        self.data_array.append(DataItem("Resource/Light.png", "光照", 450))

    def update_data(self, datapack):
        """更新指定索引的数据值"""
        print("start update data")
        for i in range(len(datapack)):
            self.data_array[i] = datapack[i]
            print(self.data_array[i])

    def get_data_by_name(self, name):
        """根据名称获取数据值"""
        for item in self.data_array:
            if item.name == name:
                return item.data_value
        return None

    def add_data_item(self, icon_path, name, data_value):
        """添加新的数据项"""
        new_item = DataItem(icon_path, name, data_value)
        self.data_array.append(new_item)

    def get_all_data(self):
        """获取所有数据项"""
        return self.data_array
