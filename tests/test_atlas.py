from pathlib import Path

from PIL import Image

from src.atlas import generate_atlas
from src.packer import PackedSprite


def test_generate_atlas(tmp_path: Path) -> None:
    sprite_path = tmp_path / "player.png"

    Image.new(
        "RGBA",
        (32, 32),
        (255, 0, 0, 255),
    ).save(sprite_path)

    sprites = [
        {
            "name": "player",
            "path": sprite_path,
            "width": 32,
            "height": 32,
        }
    ]

    packed_sprites = [
        PackedSprite(
            name="player",
            x=4,
            y=4,
            width=32,
            height=32,
        )
    ]

    output_path = tmp_path / "atlas.png"

    generate_atlas(
        sprites,
        packed_sprites,
        str(output_path),
        atlas_width=64,
        atlas_height=64,
    )

    assert output_path.exists()

    with Image.open(output_path) as atlas:
        assert atlas.size == (64, 64)
        assert atlas.mode == "RGBA"
        assert atlas.getpixel((4, 4)) == (255, 0, 0, 255)