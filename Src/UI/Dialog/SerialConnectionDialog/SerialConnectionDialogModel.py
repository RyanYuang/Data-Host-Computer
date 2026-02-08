from dataclasses import dataclass,field
from typing import Dict

from Src.Serial.SerialManager import SerialManager


@dataclass
class SerialConnectionDialogModel:
    current_port: str = ""
