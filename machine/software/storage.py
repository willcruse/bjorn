import json
from drinks import Drink

class Storage():

    def get_drinks(self):
        raise NotImplementedError
    
    def get_drink(self, label: str):
        raise NotImplementedError

    def save_drink(self, label: str, drink: Drink):
        raise NotImplementedError

    def del_drink(self, label):
        raise NotImplementedError

    def save_pump(self, index, pump):
        raise NotImplementedError

    def get_pumps(self):
        raise NotImplementedError

    def get_pump(self, index):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    def save_to_disk(self):
        raise NotImplementedError

class LocalStorage(Storage):
    def __init__(self):
        self._drinks = {}
        self._pumps = [None] * 6

    def get_drinks(self):
        return self._drinks

    def get_drink(self, label: str):
        return self._drinks.get(label)

    def save_drink(self, label: str, drink: Drink):
        self._drinks[label] = drink

    def del_drink(self, label):
        self._drinks.pop(label, None)

    def save_pump(self, index, pump):
        self._pumps[index] = pump

    def get_pumps(self):
        return self._pumps

    def get_pump(self, index):
        if 0 <= index < 6:
            return self._pumps[index]
        return None

    def to_dict(self):
        return {
            "pumps": [pump.to_json() for pump in self._pumps],
            "drinks": [drink.to_json() for _,drink in self._drinks.items()]
        }

    def save_to_disk(self):
        with open('config.json', 'w') as out_file:
            json.dump(self.to_dict())