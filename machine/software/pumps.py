from typing import List
import time

# import RPi.GPIO as GPIO

# Mock GPIO for dev on non-GPIO device
from mock import MagicMock
GPIO = MagicMock()

class Output():
    """Class representing a fluid dispenser"""
    def __init__(self, switch_pin: int, contents: str) -> None:
        self.switch_pin = switch_pin
        self.contents = contents
        self.pouring = False

        GPIO.setup(self.switch_pin, GPIO.IN)

    def __str__(self):
        return self.contents

    def _switch_active(self) -> bool:
        """Checks if the glass sled is at the pump"""
        return bool(GPIO.input(self.switch_pin))

    def pour(self, amount: int)-> bool:
        """Activate pump for given amount"""
        raise NotImplementedError

class PeristalticPump(Output):
    """Perostaltic Pump using an L298N motor controller"""
    def __init__(self, pins: List[int], switch_pin: int, contents: str) -> None:
        super().__init__(switch_pin, contents)
        self.pins = pins
        GPIO.setup(self.pins, GPIO.OUT)
    
    def pour(self, amount: int) -> bool:
        if not self._switch_active() or self.pouring:
            return False

        sleep_time = amount / (10/6) # Pumps at ~100ml/m -> 10/6 ml/s
        self.pouring = True
        GPIO.output(self.pins[0], GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(self.pins[0]. GPIO.LOW)
        self.pouring = False
        return True

class Solenoid(Output):
    """Solenoid valve output using a relay"""
    def __init__(self, pins: List[int], switch_pin: int, contents: str) -> None:
        super().__init__(switch_pin, contents)
        if len(pins) == 0:
            raise Exception("Invalid config must have at least 1 pin")
        self.activate_pin = pins[0]
        GPIO.setup(self.activate_pin, GPIO.OUT)

    def pour(self, amount: int) -> bool:
        if not self._switch_active() or self.pouring:
            return False

        sleep_time = amount / 10 # Pumps at ~10ml/s
        self.pouring = True
        GPIO.output(self.activate_pin, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(self.activate_pin. GPIO.LOW)
        self.pouring = False
        return True
