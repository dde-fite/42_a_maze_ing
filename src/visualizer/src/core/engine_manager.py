# from typing import TYPE_CHECKING
from time import time
from .mlx import MlxContext
from .window import Window
from .exceptions import (EngineNotStarted,
                         EngineElementNotFound,
                         EngineElementConflict, MlxException)
from .input import InputManager
from .x11 import keysymdef

from .scenes import BaseScene


class EngineManager:
    """When the program starts, it calls MlxContext to initialize the \
        connection with Mlx and executes the loop that keeps it running.

    It collects the update event and forwards it to the nodes of the loaded \
        scene.
    It also registers the input hook, which is later handled by Input class.

    Contains the scene switching system and window creation/destruction.

    Attributes:
        __main_window (Window | None): Main window spawned at start.
        __windows (list[Window]): List of window instances generated.
        __actual_scene (BaseScene | None): Current scene loaded.
        __scenes (list[type[BaseScene]]): List of scenes available.
        __last_frame_time (float): Time when the last frame was generated.
        __delta_time (float): Result of delta time calculation.

    Raises:
        EngineNotStarted: When trying to access an engine resource \
            without initializing the engine first.
        EngineElementConflict: For conflicts when there is a resource \
            allocated with the same name or parameters.
        EngineElementNotFound: In case of the user asks for a resource that \
            does not exist.
        MlxException: In case of an error from Mlx.
    """
    __main_window: Window | None = None
    __windows: list[Window] = []
    __actual_scene: BaseScene | None = None
    __scenes: list[type[BaseScene]]
    __last_frame_time: float = time()
    __is_exiting: bool = False

    @classmethod
    def init(cls, program_name: str, resolution: tuple[int, int],
             scenes: list[type[BaseScene]]) -> None:
        cls.__check_values(program_name, resolution, scenes)
        try:
            MlxContext.init()
            cls.__main_window = cls.create_window(program_name, resolution)
            if not cls.__main_window:
                raise MlxException("Error creating the main window")
            cls.__scenes = scenes
            cls.load_scene_by_id(0)
            MlxContext.get_mlx().mlx_do_key_autorepeatoff(
                MlxContext.get_mlx_ptr())
            MlxContext.get_mlx().mlx_loop_hook(
                MlxContext.get_mlx_ptr(),
                cls.__on_update,
                None)
            InputManager.add_listener_on_press(keysymdef.XK_Escape, cls.exit)
            MlxContext.get_mlx().mlx_loop(MlxContext.get_mlx_ptr())
        except KeyboardInterrupt:
            cls.exit()
        finally:
            MlxContext.close()

    @classmethod
    def exit(cls) -> None:
        if cls.__is_exiting:
            return
        cls.__is_exiting = True
        if cls.__actual_scene:
            cls.__actual_scene.on_unload()
        for w in cls.__windows:
            w.destroy_window()
        MlxContext.get_mlx().mlx_do_key_autorepeaton(
                MlxContext.get_mlx_ptr())
        MlxContext.get_mlx().mlx_loop_exit(MlxContext.get_mlx_ptr())

    @classmethod
    def __on_update(cls, param: None) -> None:
        try:
            cls.__last_frame_time = time()
            for w in cls.__windows:
                w.on_pre_update()
            InputManager.on_update()
            if cls.__actual_scene:
                for n in cls.__actual_scene.get_nodes():
                    n.on_update()
            for w in cls.__windows:
                w.on_update()
        except KeyboardInterrupt:
            cls.exit()

    @classmethod
    def get_delta_time(cls) -> float:
        return (time() - cls.__last_frame_time)

    @classmethod
    def get_actual_scene(cls) -> BaseScene | None:
        return cls.__actual_scene

    @classmethod
    def load_scene(cls, name: str) -> None:
        if cls.__actual_scene:
            cls.__actual_scene.on_unload()
        to_load = cls.__get_scene(name)
        if cls.__actual_scene.__class__ == to_load:
            return
        cls.__actual_scene = to_load()

    @classmethod
    def load_scene_by_id(cls, id: int) -> None:
        if cls.__actual_scene:
            cls.__actual_scene.on_unload()
        to_load = cls.__get_scene_by_id(id)
        if cls.__actual_scene.__class__ == to_load:
            return
        cls.__actual_scene = to_load()

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
            if scene.__mro__[0].__name__ == name:
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
