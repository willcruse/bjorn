import asyncio
from typing import Optional, List, Dict
import random

import RPi.GPIO as GPIO
from quart import Quart, request, jsonify
from quart_cors import cors

from config import Config
from factory import Factory
from drinks import Drink
from storage import LocalStorage

# Initial Setup
GPIO.setmode(GPIO.BOARD)

factory = Factory()
storage = LocalStorage()
config = Config("config.json")
pump_configs = config.get_pumps()
drink_configs = config.get_drinks()

for drink_config in drink_configs:
    storage.save_drink(drink_config["name"], Drink(drink_config))

for pump_index, pump_config in enumerate(pump_configs):
    storage.save_pump(pump_index, factory.pump_factory(pump_config['type'], pump_config))

app = Quart(__name__)
cors(app)

def find_drink(drinks: List[Drink], target_name: str) -> Optional[Drink]:
    for drink in drinks:
        if drink == target_name:
            return drink
    return None

def make_error(message: str):
    return {
        "error": message
    }

@app.route('/', methods=['GET'])
def base():
    return 'See documentation for API usage'

@app.route('/make', methods=['POST'])
async def make_drink():
    """
        1. Load drinks
        2. Find drink
        3. Check current config supports
        4. Generate amounts for each part
        5. Send pump instructions
        6. Return success
    """
    request_json = await request.get_json()
    if any(req_key not in request_json.keys() for req_key in ["name", "amount"]):
        return jsonify(make_error("Required Key missing"))

    drinks = storage.get_drinks()
    drink_key = find_drink(drinks.keys(), request_json["name"])
    if drink_key is None:
        return jsonify(make_error("Drink name not in database"))
    
    drink = drinks[drink_key]
    components = drink.get_components(float(request_json["amount"]))
    instructions = [] # [(pump, amount)]
    for component in components:
        for pump in storage.get_pumps():
            if pump.contents == component[0]:
                instructions.append((pump, component[1]))
                break
        
    if len(instructions) != len(components):
        return jsonify(make_error("Incorrect pump config"))

    try:
        results = await asyncio.gather(
            *[instruction[0].pour(instruction[1]) for instruction in instructions]
        )
    except Exception as e:
        return jsonify(make_error(f"Couldn't make drink: {e}"))
    if not all(results):
        return jsonify(make_error("Failed to make drink"))

    return jsonify({"success": True})

@app.route('/config', methods=['GET', 'POST'])
async def config_request():
    """Broken if not full config given"""
    if request.method == 'GET':
        return jsonify(storage.to_dict())

    required_keys = ["pumps"]
    request_json = await request.get_json()
    request_keys = set(request_json.keys())
    if not all(required_key in request_keys for required_key in required_keys):
        return make_error("Missing a required key")

    request_pumps = request_json["pumps"]
    for request_config in request_pumps:
        if request_config.get("number") is None:
            continue
        pump_keys = ["type", "contents", "pins"]
        old_pump = storage.get_pump(request_config.get("number"))
        new_config = {}
        for pump_key in pump_keys:
            new_config[pump_key] = request_config.get(pump_key)
        storage.save_pump(request_config["number"], factory.pump_factory(new_config["type"], new_config))
    return jsonify({"pumps": [pump.to_json() for pump in storage.get_pumps()]})

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = storage.get_drinks()
    drinks_json = [drink.to_json() for _, drink in drinks.items()]
    return jsonify({"drinks": drinks_json})

@app.route('/add-drink', methods=['POST'])
async def add_drink():
    request_json = await request.get_json()
    keys = set(request_json.keys())
    if not all(req_key in keys for req_key in ["name", "components"]):
        return make_error("Missing a required key")
    request_json["components"] = [(component[0], float(component[1])) for component in request_json["components"]]
    try:
        drink = Drink(request_json)
    except Exception as e:
        return make_error(str(e))

    storage.save_drink(drink.name, drink)
    return jsonify({"success": True})

@app.route('/delete-drink', methods=['POST'])
async def del_drink():
    request_json = await request.get_json()
    keys = set(request_json.keys())
    if not all(req_key in keys for req_key in ["name"]):
        return make_error("Missing a required key")

    storage.del_drink(request_json["name"])
    return jsonify({"success": True})

@app.route('/random', methods=['GET'])
async def random_drink():
    """
        1. Load drinks
        2. Find drink
        3. Check current config supports
        4. Generate amounts for each part
        5. Send pump instructions
        6. Return success
    """
    random_numbers = [random.random() for i in range(6)]
    sum_nums = sum(random_numbers)

    amounts = [(num/sum_nums)*100 for num in random_numbers]
    instructions = zip(storage.get_pumps(), amounts)

    try:
        results = await asyncio.gather(
            *[instruction[0].pour(instruction[1]) for instruction in instructions]
        )
    except Exception as e:
        return jsonify(make_error(f"Couldn't make drink: {e}"))

    if not all(results):
        return jsonify(make_error("Failed to make drink"))

    return jsonify({"success": True})

if __name__=='__main__':
    app.run(host='0.0.0.0')
