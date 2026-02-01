from typing import TYPE_CHECKING, Callable
from time import time
from .mlx import MlxContext
from .window import Window
from .exceptions import (EngineNotStarted,
                         EngineElementNotFound,
                         EngineElementConflict, MlxException)

if TYPE_CHECKING:
    from .scenes import BaseScene


class EngineManager:
    __main_window: Window | None = None
    __windows: list[Window] = []
    __actual_scene: BaseScene | None = None
    __scenes: list[type[BaseScene]]
    __last_frame_time: float = time()
    __delta_time: float = 0.0

    @classmethod
    def init(cls, program_name: str, resolution: tuple[int, int],
             scenes: list[type[BaseScene]]) -> None:
        cls.__check_values(program_name, resolution, scenes)
        MlxContext.init()
        cls.__main_window = cls.create_window(program_name, resolution)
        if not cls.__main_window:
            raise MlxException("Error creating the main window")
        cls.__scenes = scenes
        cls.load_scene_by_id(0)
        MlxContext.get_mlx().mlx_loop_hook(
            MlxContext.get_mlx_ptr(),
            cls.__on_update,
            None)
        MlxContext.get_mlx().mlx_loop(MlxContext.get_mlx_ptr())

    def exit(cls) -> None:
        if cls.__actual_scene:
            cls.__actual_scene.on_unload()
        MlxContext.get_mlx().mlx_loop_exit(MlxContext.get_mlx_ptr())
        MlxContext.close()

    @classmethod
    def __on_update(cls, param: None) -> None:
        cls.__delta_time = time() - cls.__last_frame_time
        for w in cls.__windows:
            MlxContext.get_mlx().mlx_clear_window(
                MlxContext.get_mlx_ptr(), w.get_ptr())
        if cls.__actual_scene:
            for n in cls.__actual_scene.get_nodes():
                n.expose_update()()
        cls.__last_frame_time = time()

    @classmethod
    def get_delta_time(cls) -> float:
        return cls.__delta_time

    @classmethod
    def get_actual_scene(cls) -> BaseScene | None:
        return cls.__actual_scene

    @classmethod
    def load_scene(cls, name: str) -> None:
        if cls.__actual_scene:
            cls.__actual_scene.on_unload()
        cls.__actual_scene = cls.__get_scene(name)()

    @classmethod
    def load_scene_by_id(cls, id: int) -> None:
        if cls.__actual_scene:
            cls.__actual_scene.on_unload()
        cls.__actual_scene = cls.__get_scene_by_id(id)()

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

    @classmethod
    def __get_scene(cls, name: str) -> type[BaseScene]:
        for scene in cls.__scenes:
            if type(scene).__name__ == name:
                return scene
        raise EngineElementNotFound(f"Scene '{name}' not found")

    @classmethod
    def __get_scene_by_id(cls, id: int) -> type[BaseScene]:
        return cls.__scenes[id]

    @classmethod
    def __check_values(cls, program_name: str, resolution: tuple[int, int],
                       scenes: list[type[BaseScene]]) -> None:
        if not isinstance(program_name, str):
            raise EngineNotStarted("Invalid program name: expected 'str', "
                                   f"found '{type(program_name)}'")

        if not isinstance(resolution, tuple):
            raise EngineNotStarted(
                "Invalid resolution: expected 'tuple' ([int, int]), "
                f"found: {type(resolution)}")
        i: int = 0
        for v in resolution:
            i += 1
            if i > 2:
                raise EngineNotStarted(
                    "Invalid resolution: expected 'tuple' ([int, int]), "
                    "found: 'tuple' ([...,...,...])")
            if not isinstance(v, int):
                raise EngineNotStarted(
                    "Invalid resolution: expected 'tuple' ([int, int]), "
                    "found: 'tuple' ([Any])")
