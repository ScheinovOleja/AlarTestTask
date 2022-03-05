import json

from server import create_app

app = create_app()


@app.route('/get_data/<int:pk>', methods=["GET"])
def get_correlation_data(pk):
    path = f'data/file_{pk}.json'
    with open(path, 'r') as file:
        data = json.load(file)
        sort_data = sorted(data, key=lambda item: item['id'])
    # time.sleep(1)
    return {'source': sort_data}


if __name__ == '__main__':
    app.run()
