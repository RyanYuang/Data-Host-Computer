from dataclasses import dataclass, field
from typing import List

@dataclass
class HeadModel:
    """
    Data model for the HeadView.
    """
    connection_status: bool = False
    available_ports: List[str] = field(default_factory=list)
    selected_port: str = ""
    is_alarm_triggered: bool = False
