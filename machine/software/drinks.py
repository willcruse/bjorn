from typing import Dict, List

class Drink():
    def __init__(self, config: Dict) -> None:
        """Turns component amounts into proportion of total"""
        self.name = config["name"]

        components = config["components"]
        total_amount = sum(component[1] for component in components)
        self.components = [(component[0], component[1]/total_amount) for component in components]

    def get_components(self, amount: int) -> List:
        """Returns amount to pump for each component in the drink"""
        return [(component[0], component[1]*amount) for component in self.components]


class Drinks():
    def __init__(self) -> None:
        self._drinks = []

    def __setitem__(self, index: int, value: Drink) -> None:
        self._drinks[index] = value

    def __getitem__(self, index) -> Drink:
        return self._drinks[index]
