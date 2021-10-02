from abc import ABC


class Exporter(ABC):
    """
    Abstract Base Class for generic exporting of values to a directory of
    """

    def __init__(self, path: str):
        self.path = path

    def get_path(self) -> str:
        return self.path

