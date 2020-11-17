import asyncio
from typing import Optional
from quart import Quart, request, jsonify
from quart_cors import cors

from config import Config
from factory import Factory
from drinks import Drink
from storage import LocalStorage

factory = Factory()
storage = LocalStorage()
config = Config("config.json")
pump_configs = config.get_pumps()
drink_configs = config.get_drinks()

for drink_config in drink_configs:
    storage.save_drink(drink_config["name"], drink_config)

pumps = [factory.pump_factory(pump_config['type'], pump_config) for pump_config in pump_configs]
drinks = [Drink(drink_config) for drink_config in drink_configs]

print([str(pump) for pump in pumps])


app = Quart(__name__)
cors(app)

def find_drink(drinks: list[Drink], target_name: str) -> Optional[Drink]:
    for drink in drinks:
        if drink["name"] == target_name:
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
    request_json = request.json
    if any(req_key not in request_json.keys() for req_key in ["name", "amount"]):
        return jsonify(make_error("Required Key missing"))

    drinks = storage.get_drinks()
    drink = find_drink(drinks, request_json["name"])
    if drink is None:
        return jsonify(make_error("Drink name not in database"))

    components = drink.get_components(request_json["amount"])
    instructions = [] # [(pump, amount)]
    for component in components:
        for pump in pumps:
            if pump.contents == component[0]:
                instructions.append(pump, component[1])
                break
        
    if len(instructions) != len(components):
        return jsonify(make_error("Incorrect pump config"))

    try:
        await asyncio.gather(
            *[instruction[0].pour(instructions[1]) for instruction in instructions]
        )
    except Exception as e:
        return jsonify(make_error(f"Couldn't make drink: {e}"))
    return 'Make drink'

@app.route('/config', methods=['GET', 'POST'])
def config_request():
    if request.method == 'GET':
        return jsonify(config.get_json())
    
    return 'Set config'

@app.route('/drinks', methods=['GET'])
def drinks():
    return jsonify({"drinks": storage.get_drinks()})

@app.route('/add-drink', methods=['POST'])
def add_drink():
    return 'Add new drink'

@app.route('/delete-drink', methods=['POST'])
def del_drink():
    return 'Delete drink'

if __name__=='__main__':
    app.run()
