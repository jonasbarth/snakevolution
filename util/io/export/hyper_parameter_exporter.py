import pathlib
from typing import Dict
import json

from util.io.export.exporter import Exporter


class HyperParameterExporter(Exporter):
    """
    Exporter for exporting hyper parameters
    """
    def __init__(self, path: str):
        super().__init__(path)

    def export(self, parameters: Dict) -> bool:
        """
        Exports the list of parameters to a new json file called hyperparameters.json
        :param path: the path to where the
        :param parameters:
        :return:
        """
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

        with open(self.path + "/hyperparameters.json", "w") as outfile:
            json.dump(parameters, outfile)


