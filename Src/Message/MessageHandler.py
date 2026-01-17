from abc import ABC, abstractmethod
from Src.Message.Message import Message, HandleResult

class MessageHandler(ABC):
    """
    An interface for classes that can handle messages.
    """
    @abstractmethod
    def handle(self, message: Message) -> HandleResult:
        """
        Handles a message.

        :param message: The message to handle.
        :return: A HandleResult indicating what happened.
        """
        pass
