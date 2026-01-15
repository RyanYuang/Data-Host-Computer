from typing import Any


class BasePresenter:
    """Simple base presenter that holds a reference to the view.

    Subclasses should implement `start()` to wire view events and initialize state.
    """
    def __init__(self, view: Any):
        self.view = view
        # If the view supports set_presenter, call it so view->presenter linkage exists
        if hasattr(view, "set_presenter"):
            try:
                view.set_presenter(self)
            except Exception:
                pass

    def start(self) -> None:
        """Called after wiring to perform any initialization."""
        return None
