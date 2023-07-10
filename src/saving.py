import json
from src.saving_interface import ResultsSaver


class JsonResultsSaver(ResultsSaver):
    def __init__(self, output_file):
        self.output_file = output_file

    def save_results(self, results):
        with open(self.output_file, 'w', encoding='utf-8') as out_file:
            json.dump(results, out_file, indent=2, ensure_ascii=False)
