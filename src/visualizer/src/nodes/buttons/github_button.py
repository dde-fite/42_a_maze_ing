from pathlib import Path
import webbrowser
from ...core.nodes import SpriteButton


class GithubButton(SpriteButton):
    def __init__(self, name: str = "GithubButton",
                 pos: tuple[int, int] = (1170, 573),):
        super().__init__(name, pos, Path(__file__).parent.parent.parent / "sprites" / "buttons" / "github_button.png", self.action)

    def action(self):
        webbrowser.open(
            "https://github.com/dde-fite/42_a_maze_ing",
            new=0, autoraise=True)
