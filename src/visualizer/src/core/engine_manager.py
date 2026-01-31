from .window import Window
from .exceptions import MlxException


class EngineManager:
    __windows: list[Window] = []

    @classmethod
    def create_window(cls, name: str, size: tuple[int, int]) -> Window:
        if cls.get_window(name):
            raise MlxException(f"'{name}' window already exist")
        window = Window(name, size)
        cls.__windows.append(window)
        return window

    @classmethod
    def get_window(cls, name: str) -> Window | None:
        for window in cls.__windows:
            if window.get_name() == name:
                return window
        return None

    @classmethod
    def destroy_window(cls, name: str) -> None:
        window = cls.get_window(name)
        if not window:
            raise MlxException(f"Can not destroy '{name}' because is no "
                               "instanciated")
        window.destroy_window()
