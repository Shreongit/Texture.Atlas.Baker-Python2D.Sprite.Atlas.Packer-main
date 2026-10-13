import pytest

from src.packer import pack_sprites


def test_sprites_are_sorted_by_height() -> None:
    sprites = [
        {"name": "small", "width": 20, "height": 20},
        {"name": "large", "width": 20, "height": 80},
        {"name": "medium", "width": 20, "height": 50},
    ]

    packed, _ = pack_sprites(
        sprites,
        atlas_width=200,
    )

    assert [sprite.name for sprite in packed] == [
        "large",
        "medium",
        "small",
    ]


def test_sprites_fit_inside_atlas() -> None:
    sprites = [
        {"name": "a", "width": 40, "height": 30},
        {"name": "b", "width": 30, "height": 20},
    ]

    packed, atlas_height = pack_sprites(
        sprites,
        atlas_width=100,
    )

    for sprite in packed:
        assert sprite.x + sprite.width <= 100
        assert sprite.y + sprite.height <= atlas_height


def test_sprite_wider_than_atlas_raises_error() -> None:
    sprites = [
        {"name": "large", "width": 600, "height": 100},
    ]

    with pytest.raises(ValueError, match="wider than the atlas"):
        pack_sprites(
            sprites,
            atlas_width=512,
        )


def test_invalid_atlas_width_raises_error() -> None:
    with pytest.raises(ValueError, match="Atlas width"):
        pack_sprites(
            [],
            atlas_width=0,
        )


def test_negative_padding_raises_error() -> None:
    with pytest.raises(ValueError, match="Padding"):
        pack_sprites(
            [],
            atlas_width=512,
            padding=-1,
        )