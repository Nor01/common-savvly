import json
import os
from common.exceptions.json_exceptions import *


class JsonBuilder():

    def __init__(self):
        self.j = {}
        self.l = []

    def add_parameter(self, name, value):
        self.j[name] = value
        return self

    def remove_parameter(self, name):
        if name in self.j.keys():
            del self.j[name]
        return self

    def add_list(self, name, value=[]):
        self.j[name] = value
        return self

    def get(self) -> str:
        return json.dumps(self.j)

    def to_list(self) -> str:
        return json.dumps(self.get_as_list())

    def set(self, j_str):
        self.j = json.loads(j_str)
        self.l.append(self.j)
        return self

    def update_after_set(self, name: str, value:str):
        self.l.remove(self.j)

        self.add_parameter(name, value)
        self.l.append(self.j)
        return self

    def get_value_after_set(self, name: str):
        if name in self.j.keys():
            return self.j[name]
        else:
            return None

    def raw(self) -> dict:
        return self.j

    def add_to_list(self, other=None):
        if other:
            for i in other:
                self.l.append(i)
        return self

    def get_as_list(self, other=None):
        # l = list()
        # if len(self.j) > 0:
        #    self.l.append(self.j)
        if not self.l:
            self.l.append(self.j)
        if other:
            for i in other:
                self.l.append(i)
        return self.l  # json.dumps(l)

    def from_list(self, other=None) -> str:
        # l = list()
        # if len(self.j) > 0:
        #    self.l.append(self.j)

        if other:
            for i in other:
                self.l.append(i)
        return json.dumps(self.l)

    def load_json(self, json_file):
        ''' returns a dict from json file
        Args:
            json_file (path) file to read data.
        '''
        if not os.path.exists(json_file):
            raise MissingJson(
                "json file not found ({}).".format(json_file))

        fIn = open(json_file, 'r')
        try:
            self.j = json.load(fIn)
        except ValueError as e:
            msg = "{} \n JSON File issue: {}".format(json_file, str(e))
            raise InvalidJson(msg)
        finally:
            fIn.close()

        return self

    def save_json(self, json_file):
        ''' Saves a dictionary into a json file
        Args:
            json_file (file) target file to save into
        '''

        if not os.path.dirname(json_file):
            os.makedirs(json_file)

        try:
            with open(json_file, 'w') as loadedJsn:
                json.dump(self.j, loadedJsn, sort_keys=True, indent=4)
        except IOError:
            print('IOError: No such file of directory:', json_file)

        return self

    def update_json(self, json_file):
        ''' Opens a json file, load its params,
        add new keys and save it
        '''
        if not os.path.exists(json_file):
            dictData = {}
            with open(json_file, 'w') as loadedJsn:
                json.dump(dictData, loadedJsn, sort_keys=True, indent=4)

        # opens and read json into dictData
        with open(json_file, 'r') as loadedJsn:
            dictData = json.load(loadedJsn)
            dictData.update(self.j)

        with open(json_file, 'w') as loadedJsn:
            json.dump(dictData, loadedJsn, sort_keys=True, indent=4)

        return self
