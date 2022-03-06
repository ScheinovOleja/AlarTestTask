import json
from pprint import pprint

import requests as requests


def main():
    """
    Второй вариант. GET запрос на сервер в обычном режиме.
    :return:
    """
    url = "http://localhost:5000/get_data"
    correlation_data = json.loads(requests.get(url).text)['source']
    pprint(correlation_data)


if __name__ == "__main__":
    main()
