import json

from util.io.loader import Loader


class JsonLoader(Loader):
    """
    Class for loading a json file
    """

    def __init__(self, path: str):
        super().__init__(path)
        self.data = None

    def load(self) -> bool:
        try:
            with open(self.path) as json_file:
                self.data = json.load(json_file)
                return True
        except Exception:
            print(f"json file {self.path} could not be loaded")
            return False

    def get_data(self):
        return self.data
