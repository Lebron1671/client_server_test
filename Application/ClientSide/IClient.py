from abc import ABCMeta, abstractmethod


class IClient(metaclass=ABCMeta):
    @abstractmethod
    def display(self):
        pass
