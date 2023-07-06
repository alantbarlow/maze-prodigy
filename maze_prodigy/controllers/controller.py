from abc import ABC, abstractmethod


class Controller(ABC):
    
    @abstractmethod
    def destroy():
        pass