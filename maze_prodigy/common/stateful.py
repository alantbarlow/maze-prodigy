from abc import ABC, abstractmethod


class Stateful(ABC):

    @abstractmethod
    def get_state(self):
        pass


    def set_state(self):
        subclass_name = type(self).__name__
        raise NotImplementedError(f"The 'set_state()' method has not been implemented in {subclass_name}.")
