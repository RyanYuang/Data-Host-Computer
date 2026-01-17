from dataclasses import dataclass,field
from typing import Dict

from Src.Serial.SerialManger import SerialManger


@dataclass
class SerialConnectionDialogModel:
    current_port: str = ""
