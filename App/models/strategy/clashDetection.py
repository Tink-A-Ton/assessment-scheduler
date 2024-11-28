from abc import ABC, abstractmethod


class ClashDetection(ABC):
    @abstractmethod
    def detect_clash(self, new_assessment) -> bool:
        """
        Abstract method to detect clashes for an assessment.
        Should return True if there's a clash, otherwise False.
        """
        pass
