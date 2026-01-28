from pathlib import Path


class SpriteRenderer():
    def __init__(self, file_path: Path, is_active: bool):
        self.set_file_path(file_path)
        if is_active:


    def set_file_path(self, file_path: Path):
        try:
            if not file_path.is_file():
                raise FileNotFoundError
            self.file_path = file_path
        except FileNotFoundError:
            print(f"Can't found sprite '{file_path}'")

    def render_sprite(self):


    def destroy_sprite