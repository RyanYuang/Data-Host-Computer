# STM32 串口协议实现 Prompt

> **使用方法**：将以下内容完整复制到一个新的 AI 会话中，即可让 AI 帮你完成 STM32 端的协议解析代码。

---

## Prompt 开始 👇

---

我正在做一个 **环境监测小车** 项目。上位机是 PyQt6 桌面应用，下位机是 **STM32**（HAL 库）。两者通过 UART 串口通信。

上位机部分已完成，现在需要你帮我完成 **STM32 端的串口协议解析和处理代码**。

### 一、硬件与串口配置

- MCU：STM32（请用 HAL 库风格，USART 中断接收 + 行缓冲）
- 波特率：115200
- 数据位：8，无校验，1 停止位
- 编码：纯 ASCII 文本，所有帧以 `\r\n` 结尾

### 二、通信协议规范

系统有 **三种帧**，按首字符区分：

#### 1. 上行帧：传感器数据（STM32 → PC）

格式：`@<温度>,<湿度>,<CO浓度>,<光照>\r\n`

示例：`@25.6,60.3,0.5,450\r\n`

- 温度 (float, °C)，湿度 (float, %)，CO浓度 (float, ppm)，光照 (float/int, lux)
- 发送频率：500ms~1000ms 一次

#### 2. 下行帧一：控制指令（PC → STM32）

格式：`@<指令码>\r\n`

指令码定义：
| 指令码 | 含义 |
|--------|------|
| 0 | 停止 |
| 1 | 前进 |
| 2 | 后退 |
| 3 | 左转 |
| 4 | 右转 |
| 5 | 速度 25% |
| 6 | 速度 50% |
| 7 | 速度 75% |
| 8 | 速度 100% |

示例：`@1\r\n` 表示前进，`@5\r\n` 表示速度设为 25%

#### 3. 下行帧二：阈值配置同步（PC → STM32）🆕

格式：`#T<temp_low>,<temp_high>,H<hum_low>,<hum_high>,G<co_warning>,<co_danger>,L<light_low>,<light_high>\r\n`

示例：`#T-10.0,45.0,H20.0,90.0,G30.0,50.0,L0.0,10000.0\r\n`

字段说明：
| 前缀 | 字段1 | 字段2 | 单位 |
|------|-------|-------|------|
| T | temp_low (温度下限) | temp_high (温度上限) | °C |
| H | hum_low (湿度下限) | hum_high (湿度上限) | % |
| G | co_warning (CO警告值) | co_danger (CO危险值) | ppm |
| L | light_low (光照下限) | light_high (光照上限) | lux |

- 帧首为 `#` 区别于控制指令的 `@`
- 每个字母前缀后跟两个逗号分隔的浮点数（低值在前，高值在后）
- 收到后应存入 Flash/EEPROM，并实时应用到传感器数据判断

#### 4. 上行反馈帧：阈值配置反馈（STM32 → PC）🆕

STM32 在处理阈值配置后 **必须** 返回以下三种反馈之一：

| 反馈消息 | 含义 | 何时返回 |
|---------|------|---------|
| `#OK:Config synced\r\n` | 配置同步成功 | 参数有效且已应用到 RAM / Flash |
| `#ERR:Invalid params\r\n` | 参数无效 | 低值≥高值等逻辑错误 |
| `#ERR:Parse failed\r\n` | 解析失败 | 帧格式错误、sscanf 返回值不足 8 |

**上位机会在发送配置后等待 3 秒**，若未收到反馈则提示 "设备无响应"。因此反馈必须在收到配置后立即发送。

### 三、需要你实现的功能

请帮我编写以下 STM32 C 代码模块：

1. **串口接收模块** (`uart_protocol.h` / `uart_protocol.c`)
   - 基于 USART 中断（`HAL_UART_RxCpltCallback`），逐字节接收
   - 维护行缓冲区，检测到 `\n` 时标记一帧完成
   - 缓冲区大小建议 256 字节

2. **协议解析模块** (`protocol_parser.h` / `protocol_parser.c`)
   - `Protocol_Parse(char *frame)` —— 根据首字符分发：
     - `@`：调用 `Parse_ControlCommand(frame)` 解析指令码
     - `#`：调用 `Parse_ThresholdConfig(frame)` 解析阈值配置
   - 解析出的控制指令存到结构体供主循环读取
   - 解析出的阈值存到全局配置结构体
   - **阈值解析后必须发送反馈**：
     - 成功：`#OK:Config synced\r\n`
     - 参数不合理（低值≥高值）：`#ERR:Invalid params\r\n`
     - 解析失败（sscanf != 8）：`#ERR:Parse failed\r\n`

3. **阈值存储结构体**
   ```c
   typedef struct {
       float temp_low;
       float temp_high;
       float hum_low;
       float hum_high;
       float co_warning;
       float co_danger;
       float light_low;
       float light_high;
   } ThresholdConfig_t;
   ```
   - 提供默认值初始化函数
   - 提供 Flash 读写函数（可选，先用 RAM 全局变量也行）

4. **传感器数据上报函数**
   - `void SendSensorData(float temp, float hum, float co, float light)`
   - 格式化为 `@%.1f,%.1f,%.1f,%.0f\r\n` 通过 UART 发送

5. **阈值判断函数**（可选）
   - `AlertLevel_t CheckThresholds(float temp, float hum, float co, float light)`
   - 返回当前是否超限及告警级别
   - 超限时可驱动蜂鸣器 / LED 闪烁

### 四、解析示例（参考伪代码）

```c
// 收到一帧后：
void Protocol_Parse(char *frame) {
    if (frame[0] == '@') {
        // 控制指令：@<数字>\r\n
        int cmd = atoi(&frame[1]);
        Execute_Command(cmd);
    }
    else if (frame[0] == '#') {
        // 阈值配置：#T<f>,<f>,H<f>,<f>,G<f>,<f>,L<f>,<f>\r\n
        ThresholdConfig_t cfg;
        int n = sscanf(frame, "#T%f,%f,H%f,%f,G%f,%f,L%f,%f",
               &cfg.temp_low, &cfg.temp_high,
               &cfg.hum_low, &cfg.hum_high,
               &cfg.co_warning, &cfg.co_danger,
               &cfg.light_low, &cfg.light_high);

        if (n != 8) {
            // 解析失败 → 反馈错误
            SendResponse("#ERR:Parse failed\r\n");
        }
        else if (cfg.temp_low >= cfg.temp_high ||
                 cfg.hum_low >= cfg.hum_high ||
                 cfg.co_warning >= cfg.co_danger ||
                 cfg.light_low >= cfg.light_high) {
            // 参数不合理 → 反馈错误
            SendResponse("#ERR:Invalid params\r\n");
        }
        else {
            Apply_ThresholdConfig(&cfg);
            SendResponse("#OK:Config synced\r\n");
        }
    }
}

// 发送反馈响应
void SendResponse(const char *msg) {
    HAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
}
```

### 五、代码风格要求

- 使用 STM32 HAL 库
- C99 标准
- 函数和变量命名用 `PascalCase` 或 `snake_case`（保持一致即可）
- 每个函数加注释说明用途
- 头文件用 `#ifndef` 保护
- 错误处理：解析失败时丢弃该帧，不影响后续接收

### 六、文件结构

```
Core/
├── Inc/
│   ├── uart_protocol.h
│   ├── protocol_parser.h
│   └── threshold_config.h
├── Src/
│   ├── uart_protocol.c
│   ├── protocol_parser.c
│   └── threshold_config.c
```

请按以上要求生成完整代码，包含所有头文件和源文件。

---

## Prompt 结束 👆
