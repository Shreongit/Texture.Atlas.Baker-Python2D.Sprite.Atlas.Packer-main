from pathlib import Path
from PIL import Image


def scan_sprites(directory: str) -> list[dict]:
    """
    Scan a directory for PNG sprite files and return their metadata.
    """

    sprite_directory = Path(directory)

    if not sprite_directory.exists():
        raise FileNotFoundError(
            f"Sprite directory not found: {sprite_directory}"
        )

    sprites = []

    for file_path in sorted(sprite_directory.glob("*.png")):
        with Image.open(file_path) as image:
            sprites.append(
                {
                    "name": file_path.stem,
                    "path": file_path,
                    "width": image.width,
                    "height": image.height,
                }
            )

    return sprites