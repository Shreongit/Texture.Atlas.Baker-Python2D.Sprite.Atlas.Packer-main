from pathlib import Path

from PIL import Image


def generate_atlas(
    sprites: list[dict],
    packed_sprites: list,
    output_path: str,
    atlas_width: int,
    atlas_height: int,
) -> None:
    atlas = Image.new(
        "RGBA",
        (atlas_width, atlas_height),
        (0, 0, 0, 0),
    )

    sprite_map = {
        sprite["name"]: sprite
        for sprite in sprites
    }

    for packed in packed_sprites:
        sprite = sprite_map[packed.name]

        with Image.open(sprite["path"]) as image:
            image = image.convert("RGBA")
            atlas.paste(
                image,
                (packed.x, packed.y),
                image,
            )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    atlas.save(output, "PNG")