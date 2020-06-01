import csv


class DataHolder:
    _DELIMITER = ','

    def __init__(self, data_file_path):
        with open(data_file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=self._DELIMITER)
            self.data = []

            for row in reader:
                mushroom_data = {
                    'index': int(row['index']),
                    'name_lat': row['name_lat'],
                    'name_ru': row['name_ru'],
                    'types': row['type'].split(';'),
                    'description': row['description'],
                }
                self.data.append(mushroom_data)

    def get_all(self):
        return self.data

    def get_by_index(self, index):
        return self.get('index', index)

    def get_by_lat_name(self, name):
        return self.get('name_lat', name)

    def get_by_ru_name(self, name):
        return self.get('name_ru', name)

    def get(self, key, value):
        for mushroom_data in self.data:
            if mushroom_data[key] == value:
                return mushroom_data
        return None
