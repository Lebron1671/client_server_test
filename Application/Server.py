import itertools
from Models.Person import Person


class Server:
    def __init__(self):
        self.server_data = {}

    async def add_entry(self, entry: Person):
        if entry.id not in self.server_data:
            self.server_data[entry.id] = {'Name': entry.name, 'Age': entry.age}
        else:
            raise ValueError(f'The row with id: {entry.id} already exists in table')

    async def update_entry(self, entry: Person):
        if entry.id in self.server_data:
            self.server_data[entry.id] = {'Name': entry.name, 'Age': entry.age}
        else:
            raise ValueError(f'The row with id: {entry.id} already exists in table')

    async def delete_entry(self, entry_id):
        if entry_id in self.server_data:
            del self.server_data[entry_id]
        else:
            raise ValueError(f'The row with id: {entry_id} does not exist in table')

    async def get_entries(self, start_index, end_index, data=None):
        data = data if data is not None else self.server_data
        sliced_keys = itertools.islice(data.keys(), start_index, end_index)
        return [Person(key, data[key]['Name'], data[key]['Age']) for key in sliced_keys]

    async def sort_by_column(self, column_name=None, reverse=False):
        if column_name is None:
            return dict(sorted(self.server_data.items()))
        else:
            sorted_items = sorted(self.server_data.items(), key=lambda x: x[1][column_name], reverse=reverse)
            return {key: value for key, value in sorted_items}