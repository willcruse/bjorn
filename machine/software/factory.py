import inspect
import pumps

class Discoverer:
    def __init__(self):
        self.objects= {}
        for name, obj in inspect.getmembers(pumps):
            if inspect.isclass(obj):
                self.objects[name] = obj

class Factory:
    def __init__(self):
        self._discoverer = Discoverer()

    def pump_factory(self, pump_type, pump_config):
        try:
            return self._discoverer.objects[pump_type](pump_type, pump_config['config'])
        except KeyError as exe:
            print(self._discoverer.objects)
            raise Exception("Invalid Pump Type") from exe
