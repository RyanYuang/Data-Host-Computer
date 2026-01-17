from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_view import BaseView
    from .base_model import BaseModel

class BasePresenter:
    def __init__(self, view: "BaseView", model: "BaseModel" = None):
        self._view = view
        self._model = model
        self._view.set_presenter(self)