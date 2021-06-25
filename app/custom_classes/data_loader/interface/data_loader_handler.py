from abc import ABC, abstractmethod
from typing import Any, Optional



class DataLoaderHandler(ABC):
    @abstractmethod
    def set_prev(self, handler: Any) -> Any:
        pass

    @abstractmethod
    def handle(self, request_data) -> Optional[str]:
        pass

    @abstractmethod
    def execute(self, request_data) -> Any:
        pass
