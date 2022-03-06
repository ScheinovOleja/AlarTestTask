import asyncio
import json

from codetiming import Timer

from server import create_app

app = create_app()


async def get_data_from_json(files, correlation_data):
    """

    :param files: очередь выполнения
    :param correlation_data: общая переменная для записи в нее коррелированных данных
    :return:
    """
    # Пока очередь не пуста, выполняться
    while not files.empty():
        # Удаление из очереди задачи и присвоение ее переменной
        file = await files.get()
        # Вынес путь в отдельную переменную, так как мой питон немного поломался и наотрез отказывается открывать файл,
        # когда путь прописывается таким же методом в open
        path = f'data/{file}'
        with open(path, 'r') as json_file:
            try:
                # Получение данных из файла
                response_data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                continue
            # Заполнение общего файла
            for data in response_data:
                correlation_data.append(data)


@app.route('/get_data', methods=["GET"])
async def get_correlation_data():
    """
    Обработчик данных.
    :return: коррелированные данные
    """
    correlation_data = list()
    # Создание очереди выполнения
    files = asyncio.Queue()

    # Помещение "задач" в очередь
    for file in [
        "file_1.json",
        "file_3.json",
        "file_2.json",
    ]:
        await files.put(file)

    # Запуск задач
    with Timer(text="\nОбщее затраченное время: {:.10f}"):
        # Та же ситуация, что и в первом варианте, только обработка данных на сервере
        await asyncio.gather(
            asyncio.create_task(get_data_from_json(files, correlation_data)),
            asyncio.create_task(get_data_from_json(files, correlation_data)),
            asyncio.create_task(get_data_from_json(files, correlation_data)),
        )
        # Сортировка общих данных, после выполнения
        correlation_data = sorted(correlation_data, key=lambda item: item['id'])
    return {'source': correlation_data}


if __name__ == '__main__':
    app.run()
