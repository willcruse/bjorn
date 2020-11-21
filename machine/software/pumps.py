from typing import List
import time
import asyncio

# import RPi.GPIO as GPIO

# Mock GPIO for dev on non-GPIO device
from mock import MagicMock
GPIO = MagicMock()

class Output():
    """Class representing a fluid dispenser"""
    def __init__(self, pump_type: str, config: dict) -> None:
        self.type = pump_type
        self.contents = config["contents"]
        self.pins = config["pins"]

        GPIO.setup(self.pins, GPIO.OUT)
        self.pouring = False

    def __str__(self):
        return self.contents

    def to_json(self):
        """Converts Output to a JSON friendly format"""
        return {
            "type": self.type,
            "config": {
                "contents": self.contents,
                "pins": self.pins
                }
            }

    async def pour(self, amount: int)-> bool:
        """Activate pump for given amount"""
        raise NotImplementedError

class PeristalticPump(Output):
    """Peristaltic Pump using an L298N motor controller"""
    def __init__(self, pump_type: str, config: dict) -> None:
        super().__init__(pump_type, config)

    async def pour(self, amount: int) -> bool:
        if self.pouring:
            return False

        sleep_time = amount / (10/6) # Pumps at ~100ml/m -> 10/6 ml/s
        self.pouring = True
        GPIO.output(self.pins[0], GPIO.HIGH)
        await asyncio.sleep(sleep_time)
        GPIO.output(self.pins[0]. GPIO.LOW)
        self.pouring = False
        return True

class LED(Output):
    def __init__(self, pump_type: str, config: dict) -> None:
        super().__init__(pump_type, config)
        self.pin = self.pins[0]
    
    async def pour(self, amount: int) -> bool:
        print(f"Pouring: {amount} of {self.contents}")
        if self.pouring:
            return False

        sleep_time = amount / (10/6) # Pumps at ~100ml/m -> 10/6 ml/s
        self.pouring = True
        GPIO.output(self.pin, GPIO.HIGH)
        await asyncio.sleep(sleep_time)
        GPIO.output(self.pin, GPIO.LOW) 
        self.pouring = False
        return True
