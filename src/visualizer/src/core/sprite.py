from __future__ import annotations
from typing import Any
from pathlib import Path
import numpy as np
import cv2
from .exceptions import EngineNoReference, EngineException


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

    @property
    def size(self) -> tuple[int, int]:
        return self.__size

    @property
    def image(self) -> np.ndarray:
        return self.__image

    @property
    def alpha(self) -> Any:
        return self.__alpha

    def unload_sprite(self) -> None:
        del (self.__image)
        self.__references.clear()

    def __load_sprite(self) -> None:
        if not self.__file_path:
            return
        img = cv2.imread(
            self.__file_path, flags=cv2.IMREAD_UNCHANGED)
        if img is None:
            raise EngineException("Error loading sprite at "
                                  f"{self.__file_path}")
        self.__image: np.ndarray = img
        self.__size = tuple(reversed(self.__image.shape[:2]))
        if self.__image.shape[2] == 3 or not np.any(
                                                self.__image[:, :, 3] != 255):
            self.__alpha = None
        else:
            self.__alpha = self.__image[:, :, 3:4] / 255.0
