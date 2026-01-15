"""Startup manager: 集中处理程序启动时的特殊参数和动作。

目前把原先 `--serial-test` 的处理迁移到这里，便于集中扩展其他启动参数。
"""
from typing import List, Optional
import sys

from Src.UnitTest.Serial.SerialUnitest import serial_test_mode


def run_startup(argv: List[str]) -> Optional[int]:
    """检查启动参数并在需要时执行特殊流程。

    返回要退出的整数退出码（或 None 表示继续正常启动）。
    """
    if "--serial-test" in argv:
        return serial_test_mode()
    return None


__all__ = ["run_startup"]
