from pathlib import Path
from typing import Callable, Any
from abc import ABC
from .base_node import BaseNode
from ..components import SpriteRenderer, Input
from ..components.reserved import Button


class SpriteButton(BaseNode, ABC):
    def __init__(self, name: str = "SpriteButton",
                 pos: tuple[int, int] = (0, 0),
                 file_path: Path | None = None,
                 callback: Callable[[], Any] | None = None):
        super().__init__(name, pos)
        self += (SpriteRenderer, file_path)
        self += (Input)
        self += (Button, callback)
