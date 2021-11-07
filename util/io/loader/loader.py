from abc import ABC


class Loader(ABC):
    """
    Abstract Base Class for generic loader a model
    """

    def __init__(self, path: str):
        self.path = path

    def get_path(self) -> str:
        return self.path

    def load(self) -> bool:
        pass