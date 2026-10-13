from pathlib import Path

from PIL import Image

from src.scanner import scan_sprites
from src.packer import pack_sprites
from src.atlas import generate_atlas
from src.metadata import generate_metadata


def test_complete_pipeline(tmp_path: Path) -> None:
    sprite_directory = tmp_path / "sprites"
    output_directory = tmp_path / "output"

    sprite_directory.mkdir()
    output_directory.mkdir()

    Image.new("RGBA", (32, 32), (255, 0, 0, 255)).save(
        sprite_directory / "player.png"
    )

    Image.new("RGBA", (48, 24), (0, 255, 0, 255)).save(
        sprite_directory / "enemy.png"
    )

    sprites = scan_sprites(str(sprite_directory))

    packed_sprites, atlas_height = pack_sprites(
        sprites,
        atlas_width=128,
        padding=2,
    )

    atlas_path = output_directory / "atlas.png"
    metadata_path = output_directory / "atlas.json"

    generate_atlas(
        sprites,
        packed_sprites,
        str(atlas_path),
        128,
        atlas_height,
    )

    generate_metadata(
        packed_sprites,
        atlas_path.name,
        128,
        atlas_height,
        str(metadata_path),
    )

    assert atlas_path.exists()
    assert metadata_path.exists()

    with Image.open(atlas_path) as atlas:
        assert atlas.width == 128
        assert atlas.height == atlas_height
        assert atlas.mode == "RGBA"

    assert metadata_path.stat().st_size > 0