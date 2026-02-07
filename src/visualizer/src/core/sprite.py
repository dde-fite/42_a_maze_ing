from typing import Any
from pathlib import Path
from ctypes import c_void_p
from .mlx import MlxContext
from .exceptions import MlxException, EngineNoReference


class Sprite:
    """Pool the on-demand sprite load in a unique way to avoid loading the \
        same image multiple times.

    Stores sprites in memory within classes and records who is using them.

    When a SpriteRenderer or any other component needs a sprite, it can use \
        load_sprite().
    This function checks if it already exists in memory; if it does, it simply\
        notes that it's in use, and if not, it loads it, also noting its usage.

    When the sprite is no longer needed, the component will use \
        unload_sprite() to communicate this.
    The manager will remove that usage for the sprite, and if no one is using \
        the sprite anymore, it will free it from memory.

    Attributes:
        __file_path (Path): Path to image file.
        __references (list[Any]): List of entities using the sprite.
        __size (tuple[int, int]): Size of the image in px.
        __ptr: (c_void_p | None): Pointer to the image loaded by Mlx.

    Raises:
        FileNotFoundError: If an invalid route is passed as image path.
    """
    def __init__(self, file_path: Path, reference: Any):
        if not file_path.is_file():
            raise FileNotFoundError(f"Can't found sprite '{file_path}'")
        self.__file_path: Path = file_path
        self.__references: list[Any] = []
        self.__size: tuple[int, int] = (0, 0)
        self.__ptr: c_void_p | None = None
        if reference:
            self.__references.append(reference)
        self.__load_sprite()

    def get_file_path(self) -> Path:
        return self.__file_path

    def get_references(self) -> list[Any]:
        return self.__references.copy()

    def add_reference(self, reference: Any) -> None:
        self.__references.append(reference)

    def remove_reference(self, reference: Any) -> None:
        self.__references.remove(reference)

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def get_ptr(self) -> c_void_p | None:
        return self.__ptr

    def unload_sprite(self) -> None:
        if self.__ptr:
            MlxContext.get_mlx().mlx_destroy_image(MlxContext.get_mlx_ptr(),
                                                   self.__ptr)
        self.__ptr = None
        self.__references.clear()

    def __load_sprite(self) -> None:
        if not self.__file_path:
            return
        self.__ptr, size_x, size_y = MlxContext.get_mlx(
            ).mlx_xpm_file_to_image(
                MlxContext.get_mlx_ptr(), str(self.__file_path))
        self.__size = (size_x, size_y)
        if not self.__ptr:
            raise MlxException(f"Error creating '{self.__file_path}' image")


class SpriteManager:
    """Pool the on-demand sprite load in a unique way to avoid loading the \
        same image multiple times.

    Stores sprites in memory within classes and records who is using them.

    When a SpriteRenderer or any other component needs a sprite, it can use \
        load_sprite().
    This function checks if it already exists in memory; if it does, it simply\
        notes that it's in use by that entity, and if not, it loads it, also \
            noting its usage.

    When the sprite is no longer needed, the component will use \
        unload_sprite() to communicate this.
    The manager will remove that usage for the sprite, and if no one is using \
        the sprite anymore, it will free it from memory.

    Attributes:
        __sprites (list[Sprite]): List that contains the loaded sprites.

    Raises:
        EngineNoReference: In case of passing None as a reference.
    """
    __sprites: list[Sprite] = []

    @classmethod
    def load_sprite(cls, file_path: Path, referenced_by: Any) -> Sprite:
        if not referenced_by:
            raise EngineNoReference("It is obligatory a 'referenced by' value"
                                    " for loading sprites")
        sprite = cls.get_sprite(file_path)
        if sprite:
            sprite.add_reference(referenced_by)
            return sprite
        sprite = Sprite(file_path, referenced_by)
        cls.__sprites.append(sprite)
        return sprite

    @classmethod
    def unload_sprite(cls, file_path: Path, referenced_by: Any) -> None:
        sprite = cls.get_sprite(file_path)
        if not sprite:
            return
        sprite.remove_reference(referenced_by)
        if len(sprite.get_references()) < 1:
            sprite.unload_sprite()
            cls.__sprites.remove(sprite)

    @classmethod
    def get_sprite(cls, file_path: Path) -> Sprite | None:
        for s in cls.__sprites:
            if s.get_file_path() == file_path:
                return s
        return None
