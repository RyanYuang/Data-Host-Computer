import uuid
from enum import Enum
from typing import Any

class HandleResult(Enum):
    """
    Defines the result of a message handler's attempt to process a message.
    """
    CONSUMED = 1  # The message was handled and should not be processed further.
    CONTINUE = 2  # The message was processed, but can be passed to subsequent handlers.
    SKIP = 3      # The handler chose not to process the message; it should be passed on.

class Message:
    """
    Represents a message to be dispatched through the system.
    It contains a unique ID, a type, an optional payload, and a consumed status.
    """
    def __init__(self, msg_type: str, payload: Any = None):
        self.id: str = str(uuid.uuid4())
        self.type: str = msg_type
        self.payload: Any = payload
        self.consumed: bool = False
