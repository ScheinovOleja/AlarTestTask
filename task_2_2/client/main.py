import json
from pprint import pprint

import requests as requests


def main():
    url = "http://localhost:5000/get_data"
    correlation_data = json.loads(requests.get(url).text)['source']
    pprint(sorted(correlation_data, key=lambda item: item['id']))


if __name__ == "__main__":
    main()
