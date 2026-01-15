from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .base_presenter import BasePresenter


class BaseView(Protocol):
    def set_presenter(self, presenter: "BasePresenter") -> None:
        """Attach a presenter to the view."""
        ...
