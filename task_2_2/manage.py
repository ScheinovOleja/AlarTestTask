import asyncio
import json

from codetiming import Timer
from server import create_app

app = create_app()


async def get_data_from_json(files, correlation_data):
    while not files.empty():
        file = await files.get()
        path = f'data/{file}'
        with open(path, 'r') as json_file:
            try:
                response_data = json.load(json_file)
            except json.decoder.JSONDecodeError as err:
                print(err)
                continue
            for data in response_data:
                correlation_data.append(data)


@app.route('/get_data', methods=["GET"])
async def get_correlation_data():
    correlation_data = list()
    files = asyncio.Queue()

    # Помещение задач в очередь
    for file in [
        "file_1.json",
        "file_3.json",
        "file_2.json",
    ]:
        await files.put(file)

    # Запуск задач
    with Timer(text="\nОбщее затраченное время: {:.10f}"):
        # Параллельный запуск задач
        await asyncio.gather(
            asyncio.create_task(get_data_from_json(files, correlation_data)),
            asyncio.create_task(get_data_from_json(files, correlation_data)),
            asyncio.create_task(get_data_from_json(files, correlation_data)),
        )
        correlation_data = sorted(correlation_data, key=lambda item: item['id'])
    return {'source': correlation_data}


if __name__ == '__main__':
    app.run()
