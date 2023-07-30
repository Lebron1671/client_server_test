from Application.Server import Server
from Models.Person import Person


class Client:
    def __init__(self, server: Server, start_index=0, end_index=10):
        self.server = server
        self.start_index = start_index
        self.end_index = end_index
        self.client_data = None

    async def scroll(self, direction: str):
        if direction == 'up' and self.start_index > 0:
            self.start_index -= 1
            self.end_index -= 1
        elif direction == 'down' and self.end_index < len(self.server.server_data):
            self.start_index += 1
            self.end_index += 1

        await self.display(self.client_data)

    async def sort_by_column(self, column_name=None, reverse=False):
        sorted_data = await self.server.sort_by_column(column_name, reverse)
        if column_name is not None:
            self.client_data = sorted_data
        await self.display(sorted_data)

    async def display(self, data=None):
        if data is not None:
            rows_to_display = await self.server.get_entries(self.start_index, self.end_index, data)
        else:
            rows_to_display = await self.server.get_entries(self.start_index, self.end_index)

        print("-" * 27)
        print("| ID   | Name       | Age |")
        print("-" * 27)
        for row in rows_to_display:
            print("| {:<4} | {:<10} | {:<3} |".format(row.id, row.name, row.age))
        print("-" * 27)

    async def discard(self):
        self.start_index = 0
        self.end_index = 10
        self.client_data = None
        await self.sort_by_column()

    async def change_page_size(self, new_end_index):
        self.end_index = new_end_index
        await self.display(self.client_data)

    async def pagination(self, direction: str):
        window_size = self.end_index - self.start_index

        if direction == 'next' and self.end_index < len(self.server.server_data):
            self.start_index += window_size
            self.end_index += window_size
        elif direction == 'previous' and self.start_index > 0:
            self.start_index -= window_size
            self.end_index -= window_size

        await self.display(self.client_data)

    async def add_person(self, name, age):
        last_entry_id = list(self.server.server_data)[-1]
        new_person = Person(last_entry_id + 1, name, age)
        await self.server.add_entry(new_person)

    async def update_person(self, person_id, name, age):
        person = Person(person_id, name, age)
        await self.server.update_entry(person)

    async def delete_person(self, person_id):
        await self.server.delete_entry(person_id)