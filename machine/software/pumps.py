from typing import List
import time
import asyncio

import RPi.GPIO as GPIO

# Mock GPIO for dev on non-GPIO device
#from mock import MagicMock
#GPIO = MagicMock()

class Output():
    """Class representing a fluid dispenser"""
    def __init__(self, config: dict) -> None:
        self.contents = config["contents"]
        self.pouring = False

    def __str__(self):
        return self.contents

    async def pour(self, amount: int)-> bool:
        """Activate pump for given amount"""
        raise NotImplementedError

class PeristalticPump(Output):
    """Peristaltic Pump using an L298N motor controller"""
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.pins = config["pins"]
        GPIO.setup(self.pins, GPIO.OUT)
    
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
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.pin = config["pins"][0]
        GPIO.setup(self.pin, GPIO.OUT)
    
    async def pour(self, amount: int) -> bool:
        if self.pouring:
            return False

        sleep_time = amount / (10/6) # Pumps at ~100ml/m -> 10/6 ml/s
        self.pouring = True
        GPIO.output(self.pin, GPIO.HIGH)
        await asyncio.sleep(sleep_time)
        GPIO.output(self.pin, GPIO.LOW) 
        self.pouring = False
        return True
