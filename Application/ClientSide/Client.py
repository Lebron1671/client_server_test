from abc import ABCMeta, abstractmethod

from Application.ClientSide.IClient import IClient
from Application.ServerSide.IServer import IServer
from Models.Person import Person


class Client(IClient):
    def __init__(self, server: IServer, start_index=0, end_index=10):
        self.server = server
        server.subscribe(self)
        self.start_index = start_index
        self.end_index = end_index
        self.client_data = None

    def scroll(self, direction: str):
        if direction in ['up', 'down']:
            if direction == 'up' and self.start_index > 0:
                self.start_index -= 1
                self.end_index -= 1
            elif direction == 'down' and self.end_index < self.server.length:
                self.start_index += 1
                self.end_index += 1
        else:
            raise ValueError(f'Invalid scroll direction: {direction}')

        self.display()

    def sort(self, column_name='Id', reverse=False):
        self.client_data = self.server.sort(column_name, reverse)

        self.display()

    def display(self):
        rows_to_display = self.server.get_batch_entries(self.start_index, self.end_index, self.client_data)

        divider_line = "-" * 27
        print(divider_line)
        print("| ID   | Name       | Age |")
        print(divider_line)
        for row in rows_to_display:
            print("| {:<4} | {:<10} | {:<3} |".format(row.id, row.name, row.age))
        print(divider_line)

    def discard(self):
        self.start_index, self.end_index = 0, 10
        self.client_data = None
        self.sort()

    def change_page_size(self, new_end_index):
        if new_end_index != self.end_index and new_end_index > self.start_index:
            self.end_index = new_end_index

            self.display()

    def paginate(self, direction: str):
        if direction in ['next_page', 'previous_page']:
            window_size = self.end_index - self.start_index

            if direction == 'next_page' and self.end_index < self.server.length:
                self.start_index += window_size
                self.end_index += window_size
            elif direction == 'previous_page' and self.start_index > 0:
                self.start_index -= window_size
                self.end_index -= window_size
        else:
            raise ValueError(f'Invalid pagination direction: {direction}')

        self.display()

    def add_person(self, name, age):
        new_id = self.server.get_new_id()
        new_person = Person(new_id, name, age)
        self.server.insert(new_person)

    def update_person(self, person_id, name, age):
        person = Person(person_id, name, age)
        self.server.update(person)

    def delete_person(self, person_id, name, age):
        person = Person(person_id, name, age)
        self.server.delete(person)
