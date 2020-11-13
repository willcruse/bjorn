import json
from typing import Dict, List

class Config:
    def __init__(self, file_path: str) -> None:
       with open(file_path) as json_file:
            self.json_contents = json.load(json_file)

    def get_json(self) -> Dict:
        return self.json_contents

    def get_pumps(self) -> List:
        return self.json_contents["pumps"] 
