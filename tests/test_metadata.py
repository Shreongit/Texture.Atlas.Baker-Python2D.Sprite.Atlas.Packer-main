import json

from src.packer import PackedSprite
from src.metadata import generate_metadata


def test_generate_metadata(tmp_path) -> None:
    output_file = tmp_path / "atlas.json"

    sprites = [
        PackedSprite(
            name="player",
            x=10,
            y=20,
            width=64,
            height=64,
        )
    ]

    generate_metadata(
        sprites,
        "atlas.png",
        256,
        128,
        str(output_file),
    )

    with output_file.open("r", encoding="utf-8") as file:
        metadata = json.load(file)

    assert metadata["image"] == "atlas.png"
    assert metadata["width"] == 256
    assert metadata["height"] == 128

    assert metadata["sprites"]["player"] == {
        "x": 10,
        "y": 20,
        "width": 64,
        "height": 64,
    }


def test_metadata_supports_multiple_sprites(tmp_path) -> None:
    output_file = tmp_path / "atlas.json"

    sprites = [
        PackedSprite("player", 0, 0, 64, 64),
        PackedSprite("enemy", 68, 0, 32, 48),
    ]

    generate_metadata(
        sprites,
        "atlas.png",
        128,
        64,
        str(output_file),
    )

    with output_file.open("r", encoding="utf-8") as file:
        metadata = json.load(file)

    assert len(metadata["sprites"]) == 2
    assert metadata["sprites"]["player"]["width"] == 64
    assert metadata["sprites"]["enemy"]["height"] == 48