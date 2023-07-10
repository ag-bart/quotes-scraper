from abc import ABC, abstractmethod


class ResultsSaver(ABC):
    @abstractmethod
    def save_results(self, results):
        pass
