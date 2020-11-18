import asyncio
from typing import Optional, List, Dict

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
    storage.save_drink(drink_config["name"], drink_config)

PUMPS = [factory.pump_factory(pump_config['type'], pump_config) for pump_config in pump_configs]

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
    
    drink = Drink(drinks[drink_key])
    components = drink.get_components(request_json["amount"])
    instructions = [] # [(pump, amount)]
    for component in components:
        for pump in PUMPS:
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
def config_request():
    if request.method == 'GET':
        return jsonify(config.get_json())
    
    return 'Set config'

@app.route('/drinks', methods=['GET'])
def drinks():
    return jsonify({"drinks": storage.get_drinks()})

@app.route('/add-drink', methods=['POST'])
async def add_drink():
    request_json = await request.get_json()
    keys = set(request_json.keys())
    if not all(req_key in keys for req_key in ["name", "components"]):
        return make_error("Missing a required key")

    try:
        drink = Drink(request_json)
    except Exception as e:
        return make_error(str(e))

    storage.save_drink(drink.name, drink)
    return jsonify({"success": True})

@app.route('/delete-drink', methods=['POST'])
def del_drink():
    return 'Delete drink'

if __name__=='__main__':
    app.run(host='0.0.0.0')
