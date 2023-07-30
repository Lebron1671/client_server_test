import itertools


class Server:
    def __init__(self):
        self.data = {}

    def add_row(self, row_id, row_data):
        if row_id not in self.data:
            self.data[row_id] = row_data
        else:
            raise ValueError(f'The row with id: {row_id} already exists in table')

    def update_row(self, row_id, row_updated_data):
        if row_id in self.data:
            self.data[row_id] = row_updated_data
        else:
            raise ValueError(f'The row with id: {row_id} does not exist in table')

    def delete_row(self, row_id):
        if row_id in self.data:
            del self.data[row_id]
        else:
            raise ValueError(f'The row with id: {row_id} does not exist in table')

    def get_rows_slice(self, start_index, end_index):
        sliced_keys = itertools.islice(self.data.keys(), start_index, end_index)
        return [(key, self.data[key]) for key in sliced_keys]

    def sort_by_column(self, column_name=None, reverse=False):
        if column_name is None:
            self.data = dict(sorted(self.data.items()))
        else:
            sorted_items = sorted(self.data.items(), key=lambda x: x[1][column_name], reverse=reverse)
            self.data = {key: value for key, value in sorted_items}