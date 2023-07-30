import time

from server import Server
from client import Client
import random

def generate_data(server: Server, count_row: int):
    names = ["Mike", "Aaron", "Ada", "Barney", "Ted", "Anna", "Alice", "Bob", "Nick", "Dean", "Sam",
            "Helena", "Maria", "Marta", "Brad", "Alexander", "Matilda", "Mason", "Monica", "Harper",
            "Hugh", "Hunter", "Hillary", "Esmeralda", "Ethel", "Charlie", "Shawn", "Foster", "Wyatt",
            "Walter", "Thora", "Tina", "Tania", "Teresa", "Stephany", "Scarlett", "Silvia", "Sally"]
    for i in range(1, count_row + 1):
        server.add_row(i, {"Name": f"{random.choice(names)}", "Age": random.randint(5, 90)})

def test_rows(rows_count):
    start_time = time.time()
    try:
        # Создаем сервер и добавляем данные в наше хранилище
        test_server = Server()
        generate_data(test_server, rows_count)
        #######################
        # Создаем клиент и отображаем данные по дефолту
        test_client = Client(test_server)
        print("Data after connection with default settings")
        test_client.display()
        # Иммитируем событие скроллинга вниз по таблице и выводим данные
        print("Data after scrolling to down")
        test_client.scroll("down")
        # Иммитируем событие скроллинга вниз по таблице и выводим данные
        print("Data after scrolling to up")
        test_client.scroll("up")
        # Иммитируем событие сортировки по столбцу "Age" и выводим данные
        print("Data after sort by ASC 'Age'")
        test_client.sort_by_column("Age")
        # Иммитируем событие сортировки по столбцу "Name" и выводим данные
        print("Data after sort by DESC 'Name'")
        test_client.sort_by_column("Name", True)
        # # Иммитируем событие изменения размера страницы c 10 до 50 и выводим данные
        # print("Data after changing of page size from 10 to 50")
        # test_client.change_page_size(50)
        # # Иммитируем событие изменения размера страницы c 50 до 100 и выводим данные
        # print("Data after changing of page size from 50 to 100")
        # test_client.change_page_size(100)
        # Иммитируем событие сброса сортировки и скроллинга и выводим данные
        print("Data after discard")
        test_client.discard()
        # Иммитируем событие перехода на следующую страницу и выводим данные
        print("Data after pagination to next")
        test_client.pagination('next')
        # Иммитируем событие перехода на предыдущую страницу и выводим данные
        print("Data after pagination to previous")
        test_client.pagination('previous')

    except ValueError as e:
        print(f"Error: {e}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время работы кода для {rows_count} строк данных: {execution_time:.6f} секунд ")

if __name__ == '__main__':
    test_rows(1_000_000)
