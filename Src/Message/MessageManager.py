from typing import List
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageHandler import MessageHandler

class MessageManager:
    """
    Manages and dispatches messages to a list of registered message handlers.
    """
    def __init__(self, handlers: List[MessageHandler] = None):
        self._handlers: List[MessageHandler] = handlers if handlers is not None else []

    def register(self, handler: MessageHandler):
        """
        Registers a new message handler.
        """
        if handler not in self._handlers:
            self._handlers.append(handler)

    def unregister(self, handler: MessageHandler):
        """
        Unregisters a message handler.
        """
        if handler in self._handlers:
            self._handlers.remove(handler)

    def dispatch(self, message: Message):
        """
        Dispatches a message to all registered handlers until it is consumed.
        """
        for handler in self._handlers:
            if message.consumed:
                break
            
            result = handler.handle(message)
            
            if result == HandleResult.CONSUMED:
                message.consumed = True
                break
