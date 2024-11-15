from abc import ABC, abstractmethod


class BaseTask(ABC):
    @abstractmethod
    def complete(self):
        """Отметить задачу как выполненную."""
        pass

    @abstractmethod
    def is_completed(self) -> bool:
        """Проверить, выполнена ли задача."""
        pass

    @abstractmethod
    def postpone(self, days: int):
        """Отложить задачу на заданное количество дней."""
        pass
