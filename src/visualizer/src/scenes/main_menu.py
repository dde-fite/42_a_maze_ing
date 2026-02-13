from ..core.scenes import BaseScene
from ..nodes.bg_menu import BgMenu
from ..nodes.buttons import PlayButton, CloseButton, GithubButton


class MainMenu(BaseScene):
    def __init__(self) -> None:
        super().__init__([
            BgMenu(),
            PlayButton(),
            CloseButton(),
            GithubButton()
        ])
