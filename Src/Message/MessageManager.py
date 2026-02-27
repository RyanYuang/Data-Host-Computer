from typing import List
from Src.Message.Message import Message, HandleResult
from Src.Message.MessageHandler import MessageHandler

class MessageManager:
    """
    Manages and dispatches messages to a list of registered message handlers.
    使用单例模式，确保整个应用使用同一个实例
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._handlers: List[MessageHandler] = []
        self._initialized = True

    def register(self, handler: MessageHandler):
        """
        Registers a new message handler.
        """
        if handler not in self._handlers:
            self._handlers.append(handler)
            print(f"[MessageManager] 注册 handler: {handler.__class__.__name__}, 总数: {len(self._handlers)}")

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
        # print(f"[MessageManager] 分发消息: {message.type}, 接收者数量: {len(self._handlers)}")
        for handler in self._handlers:
            if message.consumed:
                break
            
            result = handler.handle(message)
            
            if result == HandleResult.CONSUMED:
                message.consumed = True
                print(f"[MessageMessage] 消息 {message.type} 已被 {handler.__class__.__name__} 消费")
