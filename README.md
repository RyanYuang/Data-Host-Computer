# Environmental Monitoring and Control System

## English Introduction

This project is a desktop application developed using Python and the PyQt6 framework, designed to serve as a central control and monitoring station for a remote device. The application provides a user-friendly graphical interface for real-time environmental data visualization and device control, built upon a Model-View-Presenter (MVP) architecture to ensure a clean separation of concerns.

### Architecture: Model-View-Presenter (MVP)

The application is structured using the MVP design pattern to create a modular and maintainable codebase:

*   **Model:** The models are responsible for representing and managing the application's data. This includes storing sensor readings and the state of the connected device.
*   **View:** The views are responsible for the user interface and displaying data from the models. They are implemented using PyQt6 and are designed to be passive, with all logic handled by the presenter.
*   **Presenter:** The presenters act as the bridge between the models and the views. They contain the application's business logic, handle user input, update the models, and refresh the views.

### Key Features & Components

#### 1. Real-time Data Monitoring

The `DataMonitor` component provides a real-time display of environmental data from various sensors, including:

*   **Temperature**
*   **Humidity**
*   **Carbon Monoxide (CO)**
*   **Light Intensity**

Each data point is displayed with a corresponding icon and value, updating as new data is received from the device.

#### 2. Remote Device Control

The `ControlPanel` allows for remote operation of the connected device, featuring:

*   **Direction Control:** A `DirectionControlPanel` provides buttons to control the device's movement (e.g., forward, backward, left, right).
*   **Speed Control:** A `SpeedControl` interface allows the user to adjust the device's speed.
*   **Connection Status:** The control panel is disabled until a successful connection to the device is established, preventing accidental commands.

#### 3. Serial Communication

The application communicates with the hardware via a serial port, managed by the `SerialManger` class.

*   **Implementation:** It utilizes the `PyQt6.QtSerialPort` module for robust serial communication.
*   **Configuration:** The serial connection is configured with the following default parameters:
    *   **Baud Rate:** 9600
    *   **Data Bits:** 8
    *   **Stop Bits:** 1
    *   **Parity:** None
    *   **Flow Control:** None
*   **Connection Management:** The application provides functionality to list available serial ports and establish a connection to the selected device.

### Project Structure Overview

The project is organized into the following main directories:

*   `Src/`: Contains the source code for the application.
    *   `MVP/`: Base classes for the Model-View-Presenter architecture.
    *   `Serial/`: Handles serial port communication.
    *   `UI/`: Contains all the PyQt6 user interface components.
        *   `MainPage/`: The main application window, which is composed of the `Head`, `DataMonitor`, and `ControlPanel` components.
        *   `Dialog/`: UI dialogs, such as the serial connection setup.
*   `Resource/`: Contains image assets used in the UI.
*   `main.py`: The entry point of the application.

---

## 中文简介

本项目是一个使用Python和PyQt6框架开发的桌面应用程序，旨在作为一个远程设备的中央控制和监控站。该应用程序提供了一个用户友好的图形界面，用于实时环境数据显示和设备控制，并采用模型-视图-表示者（MVP）架构，以确保清晰的关注点分离。

### 架构: 模型-视图-表示者 (MVP)

该应用程序采用MVP设计模式，以创建一个模块化且可维护的代码库：

*   **模型 (Model):** 模型负责表示和管理应用程序的数据。这包括存储传感器读数和所连接设备的状态。
*   **视图 (View):** 视图负责用户界面和显示模型中的数据。它们使用PyQt6实现，并被设计为被动的，所有逻辑都由表示者处理。
*   **表示者 (Presenter):** 表示者充当模型和视图之间的桥梁。它们包含应用程序的业务逻辑，处理用户输入，更新模型并刷新视图。

### 主要功能和组件

#### 1. 实时数据监控

`DataMonitor` 组件提供来自各种传感器的环境数据的实时显示，包括：

*   **温度**
*   **湿度**
*   **一氧化碳 (CO)**
*   **光照强度**

每个数据点都与相应的图标和值一起显示，并随着从设备接收到新数据而更新。

#### 2. 远程设备控制

`ControlPanel` 允许远程操作所连接的设备，具有以下特点：

*   **方向控制:** `DirectionControlPanel` 提供按钮来控制设备的移动（例如，前进、后退、左、右）。
*   **速度控制:** `SpeedControl` 界面允许用户调整设备的速度。
*   **连接状态:** 在与设备成功建立连接之前，控制面板是禁用的，以防止意外的命令。

#### 3. 串口通信

该应用程序通过串行端口与硬件通信，由 `SerialManger` 类管理。

*   **实现:** 它利用 `PyQt6.QtSerialPort` 模块进行稳健的串行通信。
*   **配置:** 串行连接配置了以下默认参数：
    *   **波特率:** 9600
    *   **数据位:** 8
    *   **停止位:** 1
    *   **奇偶校验:** 无
    *   **流控制:** 无
*   **连接管理:** 应用程序提供列出可用串行端口并与所选设备建立连接的功能。

### 项目结构概览

该项目被组织成以下主要目录：

*   `Src/`: 包含应用程序的源代码。
    *   `MVP/`: MVP架构的基类。
    *   `Serial/`: 处理串口通信。
    *   `UI/`: 包含所有的PyQt6用户界面组件。
        *   `MainPage/`: 主应用程序窗口，由 `Head`、`DataMonitor` 和 `ControlPanel` 组件组成。
        *   `Dialog/`: UI对话框，例如串行连接设置。
*   `Resource/`: 包含UI中使用的图像资源。
*   `main.py`: 应用程序的入口点。
