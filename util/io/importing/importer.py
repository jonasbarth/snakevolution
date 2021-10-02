from abc import ABC


class Importer(ABC):
    """
    Abstract Base Class for generic importing a model
    """

    def __init__(self, path: str):
        self.path = path

    def get_path(self) -> str:
        return self.path

    def import_model(self):
        pass