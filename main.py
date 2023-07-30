import asyncio
import time
from Application.Server import Server
from Application.Client import Client
import random
from Models.Person import Person


async def generate_data(server: Server, count_row: int):
    names = ["Mike", "Aaron", "Ada", "Barney", "Ted", "Anna", "Alice", "Bob", "Nick", "Dean", "Sam",
            "Helena", "Maria", "Marta", "Brad", "Alexander", "Matilda", "Mason", "Monica", "Harper",
            "Hugh", "Hunter", "Hillary", "Esmeralda", "Ethel", "Charlie", "Shawn", "Foster", "Wyatt",
            "Walter", "Thora", "Tina", "Tania", "Teresa", "Stephany", "Scarlett", "Silvia", "Sally"]
    for i in range(1, count_row + 1):
        await server.add_entry(Person(i, random.choice(names), random.randint(5, 90)))

async def test_rows(rows_count):
    global start_time_test
    try:
        # Создаем сервер и добавляем данные в наше хранилище
        test_server = Server()
        start_time_prep = time.time()
        await generate_data(test_server, rows_count)
        end_time_prep = time.time()
        execution_time = end_time_prep - start_time_prep
        print(f"Время генерации данных для {rows_count} строк данных: {execution_time:.6f} секунд ")
        #######################
        # Создаем клиент и отображаем данные по дефолту
        start_time_test = time.time()
        test_client = Client(test_server)
        print("Data after connection with default settings")
        await test_client.display()
        # Иммитируем событие скроллинга вниз по таблице и выводим данные
        print("Data after scrolling to down")
        await test_client.scroll("down")
        # Иммитируем событие скроллинга вниз по таблице и выводим данные
        print("Data after scrolling to up")
        await test_client.scroll("up")
        # Иммитируем событие сортировки по столбцу "Age" и выводим данные
        print("Data after sort by ASC 'Age'")
        await test_client.sort_by_column("Age")
        # Иммитируем событие сортировки по столбцу "Name" и выводим данные
        print("Data after sort by DESC 'Name'")
        await test_client.sort_by_column("Name", True)
        # Иммитируем событие изменения размера страницы c 10 до 50 и выводим данные
        print("Data after changing of page size from 10 to 50")
        await test_client.change_page_size(50)
        # Иммитируем событие изменения размера страницы c 50 до 100 и выводим данные
        print("Data after changing of page size from 50 to 100")
        await test_client.change_page_size(100)
        # Иммитируем событие перехода на следующую страницу и выводим данные
        print("Data after pagination to next")
        await test_client.pagination('next')
        # Иммитируем событие перехода на предыдущую страницу и выводим данные
        print("Data after pagination to previous")
        await test_client.pagination('previous')
        # Иммитируем событие сброса сортировки и скроллинга и выводим данные
        print("Data after discard")
        await test_client.discard()

    except ValueError as e:
        print(f"Error: {e}")
    end_time_test = time.time()
    execution_time = end_time_test - start_time_test
    print(f"Время работы кода для {rows_count} строк данных: {execution_time:.6f} секунд ")

def main():
    asyncio.run(test_rows(1_000_000))

if __name__ == '__main__':
    main()