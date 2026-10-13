import json
from pathlib import Path


def generate_metadata(
    packed_sprites: list,
    atlas_filename: str,
    atlas_width: int,
    atlas_height: int,
    output_path: str,
) -> None:
    metadata = {
        "image": atlas_filename,
        "width": atlas_width,
        "height": atlas_height,
        "sprites": {},
    }

    for sprite in packed_sprites:
        metadata["sprites"][sprite.name] = {
            "x": sprite.x,
            "y": sprite.y,
            "width": sprite.width,
            "height": sprite.height,
        }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)