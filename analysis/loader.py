class Loader:
    """
    Class for loading fitness data
    """
    def __init__(self, path: str):
        self.path = path

    def get_path(self) -> str:
        return self.path

    def load(self) -> bool:
        pass
