import time
import random
from Application.ClientSide.Client import Client
from Application.ServerSide.IServer import IServer
from Application.ServerSide.Server import Server
from Models.Person import Person


def generate_data(server: IServer, count_row: int):
    names = ["Mike", "Aaron", "Ada", "Barney", "Ted", "Anna", "Alice", "Bob", "Nick", "Dean", "Sam",
            "Helena", "Maria", "Marta", "Brad", "Alexander", "Matilda", "Mason", "Monica", "Harper",
            "Hugh", "Hunter", "Hillary", "Esmeralda", "Ethel", "Charlie", "Shawn", "Foster", "Wyatt",
            "Walter", "Thora", "Tina", "Tania", "Teresa", "Stephany", "Scarlett", "Silvia", "Sally"]
    for i in range(1, count_row + 1):
        server.insert(Person(i, random.choice(names), random.randint(5, 90)))


def test_1(rows_count):
    global start_time_test
    try:
        # Создаем сервер и добавляем данные в наше хранилище
        test_server = Server()
        start_time_prep = time.time()
        generate_data(test_server, rows_count)
        end_time_prep = time.time()
        execution_time = end_time_prep - start_time_prep
        print(f"Время генерации данных для {rows_count} строк данных: {execution_time:.6f} секунд ")
        #######################
        # Создаем клиент и отображаем данные по дефолту
        start_time_test = time.time()
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
        test_client.sort("Age")
        # Иммитируем событие сортировки по столбцу "Name" и выводим данные
        print("Data after sort by DESC 'Name'")
        test_client.sort("Name", True)
        # Иммитируем событие изменения размера страницы c 10 до 50 и выводим данные
        print("Data after changing of page size from 10 to 50")
        test_client.change_page_size(50)
        # Иммитируем событие изменения размера страницы c 50 до 100 и выводим данные
        print("Data after changing of page size from 50 to 100")
        test_client.change_page_size(100)
        # Иммитируем событие перехода на следующую страницу и выводим данные
        print("Data after pagination to next page")
        test_client.paginate('next_page')
        # Иммитируем событие перехода на предыдущую страницу и выводим данные
        print("Data after pagination to previous page")
        test_client.paginate('previous_page')
        # Иммитируем событие сброса сортировки и скроллинга и выводим данные
        print("Data after discard")
        test_client.discard()

    except ValueError as e:
        print(f"Error: {e}")
    end_time_test = time.time()
    execution_time = end_time_test - start_time_test
    print(f"Время работы кода для {rows_count} строк данных: {execution_time:.6f} секунд ")


def test_2(rows_count):
    server = Server()
    start_time_prep = time.time()
    generate_data(server, rows_count)
    end_time_prep = time.time()
    execution_time = end_time_prep - start_time_prep
    print(f"Время генерации данных для {rows_count} строк данных: {execution_time:.6f} секунд ")
    test_client = Client(server, 0, 30)
    print("Data after connection with default settings")
    test_client.display()
    print('Add person')
    server.insert(Person(21, 'Nick', 27))
    print('Update person')
    server.update(Person(21, 'Ivan', 61))
    print('Delete person')
    server.delete(Person(21, 'Ivan', 61))


def main():
    test_1(10_000_000)
    #test_2(30)


if __name__ == '__main__':
    main()
