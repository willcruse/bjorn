from drinks import Drink

class Storage():

    def get_drinks(self):
        raise NotImplementedError
    
    def get_drink(self, label: str):
        raise NotImplementedError

    def save_drink(self, label: str, drink: Drink):
        raise NotImplementedError


class LocalStorage(Storage):
    def __init__(self):
        self._drinks = {}

    def get_drinks(self):
        return self._drinks

    def get_drink(self, label: str):
        return self._drinks.get(label)

    def save_drink(self, label: str, drink: Drink):
        self._drinks[label] = drink