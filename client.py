from server import Server


class Client:
    def __init__(self, server: Server, start_index=0, end_index=10):
        self.server = server
        self.start_index = start_index
        self.end_index = end_index

    def scroll(self, direction: str):
        if direction == 'up' and self.start_index > 0:
            self.start_index -= 1
            self.end_index -= 1
        elif direction == 'down' and self.end_index < len(self.server.data):
            self.start_index += 1
            self.end_index += 1

        self.display()

    def sort_by_column(self, column_name=None, reverse=False):
        self.server.sort_by_column(column_name, reverse)
        self.display()

    def display(self):
        rows_to_display = self.server.get_rows_slice(self.start_index, self.end_index)

        print("-" * 27)
        print("| ID   | Name       | Age |")
        print("-" * 27)
        for row in rows_to_display:
            print("| {:<4} | {:<10} | {:<3} |".format(row[0], row[1]['Name'], row[1]['Age']))
        print("-" * 27)

    def discard(self):
        self.start_index = 0
        self.end_index = 10
        self.sort_by_column()

    def change_page_size(self, new_end_index):
        self.end_index = new_end_index
        self.display()

    def pagination(self, direction: str):
        window_size = self.end_index - self.start_index

        if direction == 'next' and self.end_index < len(self.server.data):
            self.start_index += window_size
            self.end_index += window_size
        elif direction == 'previous' and self.start_index > 0:
            self.start_index -= window_size
            self.end_index -= window_size

        self.display()