import sys
import threading
from PyQt6 import QtCore
from PyQt6.QtCore import QCoreApplication
import Src.Serial.SerialManger as SerialManger


def serial_test_mode():
	"""交互式串口测试：在终端选择串口、发送内容并打印接收数据。

	在主线程中只需调用 `serial_test_mode()` 即可进入交互模式。
	"""
	app = QCoreApplication(sys.argv)
	sm = SerialManger.SerialManger()

	ports = sm.GetSerialList()
	if not ports:
		print("未检测到串口。请连接设备后重试。")
		return 1

	print("可用串口:")
	for idx, p in enumerate(ports):
		try:
			desc = p.description() if hasattr(p, 'description') else ''
		except Exception:
			desc = ''
		print(f"  [{idx}] {p.portName()} {desc}")

	sel = input("输入端口索引（回车选择0）: ")
	try:
		idx = int(sel) if sel.strip() != "" else 0
	except Exception:
		idx = 0
	if idx < 0 or idx >= len(ports):
		print("索引无效，使用第一个端口")
		idx = 0

	port_name = ports[idx].portName()
	print(f"尝试打开: {port_name}")
	ok = sm.OpenPortByName(port_name)
	if not ok:
		print("打开串口失败")
		return 1

	def on_ready_read():
		try:
			qba = sm.readAll()
			data = bytes(qba)
			try:
				text = data.decode('utf-8', errors='replace')
			except Exception:
				text = repr(data)
			print(f"<-- 收到 ({len(data)} bytes): {text}")
		except Exception as e:
			print(f"read error: {e}")

	sm.readyRead.connect(on_ready_read)

	class Dispatcher(QtCore.QObject):
		send = QtCore.pyqtSignal(str)
		close_req = QtCore.pyqtSignal()

		def __init__(self, serial_mgr):
			super().__init__()
			self.sm = serial_mgr
			self.send.connect(self._on_send)
			self.close_req.connect(self._on_close)

		@QtCore.pyqtSlot(str)
		def _on_send(self, txt: str):
			try:
				self.sm.write((txt + '\n').encode())
				print(f"--> 发送: {txt}")
			except Exception as e:
				print(f"send error: {e}")

		@QtCore.pyqtSlot()
		def _on_close(self):
			try:
				self.sm.ClosePort()
			except Exception:
				pass
			QCoreApplication.quit()

	dispatcher = Dispatcher(sm)

	# stdin 读取线程，用于向串口发送数据；通过信号请求在主线程执行写/关闭操作
	def stdin_loop():
		print("输入要发送的文本并回车。输入 exit 退出。")
		while True:
			try:
				line = sys.stdin.readline()
				if not line:
					break
				txt = line.rstrip('\n')
				if txt.lower() == 'exit':
					break
				if txt == '':
					continue
				dispatcher.send.emit(txt)
			except Exception:
				break
		dispatcher.close_req.emit()

	t = threading.Thread(target=stdin_loop, daemon=True)
	t.start()

	try:
		app.exec()
	except KeyboardInterrupt:
		pass
	print("串口测试结束")
	return 0


if __name__ == '__main__':
	sys.exit(serial_test_mode())

