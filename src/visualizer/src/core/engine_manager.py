from .mlx import MlxContext
from .window import Window
from .exceptions import (EngineNotStarted, EngineElementNotFound,
                         EngineElementConflict)


class EngineManager:
    __main_window: Window | None = None
    __windows: list[Window] = []

    @classmethod
    def init_engine(cls, program_name: str, resolution: tuple[int, int]
                    ) -> None:
        MlxContext.init()
        cls.__main_window = cls.create_window(program_name, resolution)

    @classmethod
    def create_window(cls, name: str, size: tuple[int, int]
                      ) -> Window:
        if cls.get_window(name):
            raise EngineElementConflict(f"'{name}' window already exist")
        window = Window(name, size)
        cls.__windows.append(window)
        return window

    @classmethod
    def get_main_window(cls) -> Window:
        if not cls.__main_window:
            raise EngineNotStarted("Engine it is not started")
        return cls.__main_window

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
            raise EngineElementNotFound(f"Can not destroy '{name}' because is "
                                        "no instanciated")
        window.destroy_window()
