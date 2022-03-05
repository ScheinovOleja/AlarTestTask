import asyncio
import json
from pprint import pprint

import aiohttp
from codetiming import Timer

correlation_data = list()


async def get_from_flask(work_queue):
    global correlation_data
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            async with session.get(url, timeout=2) as response:
                try:
                    response_data = json.loads(await response.text())['source']
                except json.decoder.JSONDecodeError:
                    continue
                for data in response_data:
                    correlation_data.append(data)


async def main():
    """
    Основная точка входа в программу
    """

    # Создание очереди
    work_queue = asyncio.Queue()

    # Помещение задач в очередь
    for url in [
        "http://localhost:5000/get_data/2",
        "http://localhost:5000/get_data/1",
        "http://localhost:5000/get_data/3",
    ]:
        await work_queue.put(url)

    # Запуск задач
    with Timer(text="\nОбщее затраченное время: {:.10f}"):
        # Параллельный запуск задач
        await asyncio.gather(
            asyncio.create_task(get_from_flask(work_queue)),
            asyncio.create_task(get_from_flask(work_queue)),
            asyncio.create_task(get_from_flask(work_queue)),
        )
        # Вывод отсортированных данных в консоль
        pprint(sorted(correlation_data, key=lambda item: item['id']))


if __name__ == "__main__":
    asyncio.run(main())
