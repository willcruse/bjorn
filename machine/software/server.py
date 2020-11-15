import asyncio
from quart import Quart, request, jsonify
from quart_cors import cors

from config import Config
from factory import Factory
from drinks import Drink

factory = Factory()

config = Config("config.json")
pump_configs = config.get_pumps()
drink_configs = config.get_drinks()

pumps = [factory.pump_factory(pump_config['type'], pump_config) for pump_config in pump_configs]
drinks = [Drink(drink_config) for drink_config in drink_configs]

print([str(pump) for pump in pumps])



app = Quart(__name__)
cors(app)

def make_error(message: str):
    return {
        "error": message
    }

@app.route('/', methods=['GET'])
def base():
    return 'See documentation for API usage'

@app.route('/make', methods=['GET', 'POST'])
async def make_drink():
    """
        1. Load drinks
        2. Find drink
        3. Check current config supports
        4. Generate amounts for each part
        5. Send pump instructions
        6. Return success
    """

    instructions = [] # [(pump, amount)]
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
    return 'List of drinks'

@app.route('/add-drink', methods=['POST'])
def add_drink():
    return 'Add new drink'

@app.route('/delete-drink', methods=['POST'])
def del_drink():
    return 'Delete drink'

if __name__=='__main__':
    app.run()
"""machine_address = socket.gethostbyname(socket.getfqdn())
pumping = False
print(f"Machine Running at IP {machine_address}")
app.run(debug=True, port=80, host='0.0.0.0')"""