import asyncio
import json
from pprint import pprint

import aiohttp
from codetiming import Timer

correlation_data = list()


async def get_from_flask(work_queue):
    """
    Функция запроса на сервер и формирования данных.
    :param work_queue: очередь задач
    :return:
    """
    global correlation_data
    # Создание асинхронной сессии
    async with aiohttp.ClientSession() as session:
        # Цикл, пока очередь задач не пуста
        while not work_queue.empty():
            # Удаление задачи из очереди и присвоение ее в переменную
            url = await work_queue.get()
            # GET запрос на сервер с таймаутом 2 секунды
            async with session.get(url, timeout=2) as response:
                # Если пришли пустые данные, игнор и продолжение выполнения
                try:
                    # Запись данных, пришедших с сервера
                    response_data = json.loads(await response.text())['source']
                except json.decoder.JSONDecodeError:
                    continue
                # Формирование общих данных из 3-х источников в глобальную переменную
                for data in response_data:
                    correlation_data.append(data)


async def main():
    # Создание очереди выполнения
    work_queue = asyncio.Queue()
    # Помещение "задач" в очередь. Расположил специально не по порядку.
    for url in [
        "http://localhost:5000/get_data/2",
        "http://localhost:5000/get_data/1",
        "http://localhost:5000/get_data/3",
    ]:
        await work_queue.put(url)

    # Запуск задач. Timer использую только для отслеживания времени выполнения. Удобно же)
    with Timer(text="\n\nОбщее затраченное время: {:.10f}"):
        # Запуск задач
        # Создание "асинхронности". Создав 1 задачу в gather, выполнение будет синхронным, по порядку, поэтому их 3)
        await asyncio.gather(
            asyncio.create_task(get_from_flask(work_queue)),
            asyncio.create_task(get_from_flask(work_queue)),
            asyncio.create_task(get_from_flask(work_queue)),
        )
        # Вывод отсортированных данных в консоль
        pprint(sorted(correlation_data, key=lambda item: item['id']))


if __name__ == "__main__":
    asyncio.run(main())
