import json

from server import create_app

app = create_app()


@app.route('/get_data/<int:pk>', methods=["GET"])
def get_correlation_data(pk):
    """
    Взятие данных из нужного источника и отдача обратно этих данных.
    :param pk: id источника.
    :return:
    """
    path = f'data/file_{pk}.json'
    with open(path, 'r') as file:
        data = json.load(file)
    # Оставил для тестирования таймаута
    # time.sleep(2)
    return {'source': data}


if __name__ == '__main__':
    app.run()
