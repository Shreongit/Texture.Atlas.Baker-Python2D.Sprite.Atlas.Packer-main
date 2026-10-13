from dataclasses import dataclass


@dataclass
class PackedSprite:
    name: str
    x: int
    y: int
    width: int
    height: int


def pack_sprites(
    sprites: list[dict],
    atlas_width: int,
    padding: int = 0,
) -> tuple[list[PackedSprite], int]:
    """
    Pack sprites using the Next-Fit Decreasing Height algorithm.

    Sprites are sorted from tallest to shortest and placed
    from left to right. When a sprite no longer fits on the
    current row, a new row is started.
    """

    if atlas_width <= 0:
        raise ValueError("Atlas width must be greater than zero.")

    if padding < 0:
        raise ValueError("Padding cannot be negative.")

    sorted_sprites = sorted(
        sprites,
        key=lambda sprite: sprite["height"],
        reverse=True,
    )

    packed = []

    current_x = padding
    current_y = padding
    current_row_height = 0

    for sprite in sorted_sprites:
        width = sprite["width"]
        height = sprite["height"]

        if width + (padding * 2) > atlas_width:
            raise ValueError(
                f"Sprite '{sprite['name']}' is wider than the atlas."
            )

        # Start a new row if the sprite does not fit.
        if current_x + width + padding > atlas_width:
            current_x = padding
            current_y += current_row_height + padding
            current_row_height = 0

        packed.append(
            PackedSprite(
                name=sprite["name"],
                x=current_x,
                y=current_y,
                width=width,
                height=height,
            )
        )

        current_x += width + padding
        current_row_height = max(current_row_height, height)

    atlas_height = current_y + current_row_height + padding

    return packed, atlas_height