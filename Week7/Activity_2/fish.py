from abc import ABC, abstractmethod

class Fish(ABC):
    # Abstract base class for all fish types.
    @abstractmethod
    def add_fish(self, kind=None):
        pass
    
