from pathlib import Path
from ..maze_visualizer import MlxManager, MlxWindow
from ..exceptions import MlxException
from base_component import BaseComponent


class SpriteRenderer(BaseComponent):
    def __init__(self, pos: tuple[int, int], file_path: Path, is_active: bool,
                 window: MlxWindow):
        super().__init__(pos)
        self.__file_path: Path | None = None
        self.__is_active: bool = False
        self.__ptr: int | None = None
        self.__window: MlxWindow = window
        self.set_file_path(file_path)
        self.set_active(is_active)

    def get_file_path(self) -> Path | None:
        return self.__file_path

    def set_file_path(self, file_path: Path) -> None:
        try:
            if not file_path.is_file():
                raise FileNotFoundError("Can't found sprite '{file_path}'")
            self.__file_path = file_path
        except FileNotFoundError as e:
            print(f"{e.args}")

    def get_active(self) -> bool:
        return self.__is_active

    def set_active(self, is_active: bool) -> None:
        if is_active and not self.__is_active:
            self.__render_sprite()
        elif not is_active and self.__is_active:
            self.__destroy_sprite()

    def get_window(self) -> MlxWindow:
        return self.__window

    def set_window(self, window: MlxWindow) -> None:
        self.__window = window

    def set_pos(self, pos: tuple[int, int]) -> None:
        self._pos = pos
        if self.__is_active:
            self.set_active(False)
            self.set_active(True)

    def __render_sprite(self) -> None:
        self.__ptr = MlxManager.get_mlx().mlx_xpm_file_to_image(
            self.__window.get_ptr(), self.__file_path)
        if not self.__ptr:
            raise MlxException(f"Error creating '{self.__file_path}' image")
        MlxManager.get_mlx().mlx_put_image_to_window(
            MlxManager.get_mlx_ptr(), self.__window.get_ptr(),
            self.__file_path, self.__pos[0], self.__pos[0])

    def __destroy_sprite(self) -> None:
        MlxManager.get_mlx().mlx_destroy_image(self.__ptr)
