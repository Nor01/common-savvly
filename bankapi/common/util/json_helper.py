
from common.util.json_builder import JsonBuilder
from common.util.utility_functions import find_file_path


class JsonHelper:
    def __init__(self):
        self.j = JsonBuilder()
        self.raw = {}


    def load_file(self, json_file):

        self.j = self.j.load_json(json_file)
        self.raw = self.j.raw()

        #print(len(self.raw['personaTemplates']))

    def json_extract(self, key):
        """Recursively fetch values from nested JSON."""
        arr = set()
        obj = self.raw
        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        #arr.append(v)
                        arr.add(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        values = extract(obj, arr, key)
        return values

if __name__ == '__main__':
    p = find_file_path("SavvlyFullData.json", "../")
    j = JsonHelper()
    j.load_file(p)
    f = j.json_extract("crumb")
    f = sorted(f)
    print(f)
    for i in f:
        print(i.split("."))

