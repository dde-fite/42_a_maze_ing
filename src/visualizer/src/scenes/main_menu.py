from ..core.scenes import BaseScene
from ..nodes import BgMenu
from ..nodes.buttons import PlayButton


class MainMenu(BaseScene):
    def __init__(self) -> None:
        super().__init__([
            BgMenu(),
            PlayButton(),
        ])
