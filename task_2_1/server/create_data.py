import json
import random


def create():
    data_1 = []
    data_2 = []
    data_3 = []
    all_data = list(range(1, 61))
    random.shuffle(all_data)
    for id_test in all_data:
        if 1 <= id_test <= 10 or 31 <= id_test <= 40:
            data_1.append({
                'id': id_test,
                'content': f'Test data 1 in {id_test}'
            })
        elif 11 <= id_test <= 20 or 41 <= id_test <= 50:
            data_2.append({
                'id': id_test,
                'content': f'Test data 2 in {id_test}'
            })
        elif 21 <= id_test <= 30 or 51 <= id_test <= 60:
            data_3.append({
                'id': id_test,
                'content': f'Test data 3 in {id_test}'
            })
    with open('data/file_1.json', 'w', encoding='utf-8') as file:
        json.dump(data_1, file)
    with open('data/file_2.json', 'w', encoding='utf-8') as file:
        json.dump(data_2, file)
    with open('data/file_3.json', 'w', encoding='utf-8') as file:
        json.dump(data_3, file)


if __name__ == '__main__':
    create()
