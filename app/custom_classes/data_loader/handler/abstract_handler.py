from abc import abstractmethod
from typing import Any

from app.custom_classes.data_loader.interface.data_loader_handler import DataLoaderHandler


class AbstractHandler(DataLoaderHandler):
    _next_handler: DataLoaderHandler = None

    def set_prev(self, handler: DataLoaderHandler) -> DataLoaderHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request_data: Any) -> Any:
        if self._next_handler is not None:
            response = self._next_handler.handle(request_data)
            if response:
                return self.execute(response)
        else:
            return self.execute(request_data)
