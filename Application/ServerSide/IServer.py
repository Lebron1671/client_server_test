from abc import ABCMeta, abstractmethod

from Models.Person import Person


class IServer(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.length = 0

    def subscribe(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

    @abstractmethod
    def insert(self, person: Person):
        pass

    @abstractmethod
    def update(self, person: Person):
        pass

    @abstractmethod
    def delete(self, person: Person):
        pass

    @abstractmethod
    def get_new_id(self):
        pass

    @abstractmethod
    def get_batch_entries(self, start_index: int, end_index: int, client_data=None):
        pass

    @abstractmethod
    def sort(self, column_name='Id', desc=False):
        pass
