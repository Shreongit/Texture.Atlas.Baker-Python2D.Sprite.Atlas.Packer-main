import argparse
from pathlib import Path

from src.scanner import scan_sprites
from src.packer import pack_sprites
from src.atlas import generate_atlas
from src.metadata import generate_metadata


DEFAULT_INPUT = "assets/sprites"
DEFAULT_OUTPUT = "output"
DEFAULT_ATLAS_WIDTH = 2048
DEFAULT_PADDING = 2


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pack PNG sprites into a texture atlas."
    )

    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Directory containing PNG sprites.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Directory for generated atlas files.",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_ATLAS_WIDTH,
        help="Atlas width in pixels.",
    )

    parser.add_argument(
        "--padding",
        type=int,
        default=DEFAULT_PADDING,
        help="Padding between sprites in pixels.",
    )

    args = parser.parse_args()

    if args.width <= 0:
        parser.error("--width must be greater than 0.")

    if args.padding < 0:
        parser.error("--padding cannot be negative.")

    input_directory = Path(args.input)

    if not input_directory.exists():
        parser.error(f"Input directory does not exist: {input_directory}")

    if not input_directory.is_dir():
        parser.error(f"Input path is not a directory: {input_directory}")

    print("Texture Atlas Baker")
    print("-" * 20)

    sprites = scan_sprites(args.input)

    if not sprites:
        print("No PNG sprites found.")
        return

    print(f"Found {len(sprites)} sprites.")

    packed_sprites, atlas_height = pack_sprites(
        sprites,
        atlas_width=args.width,
        padding=args.padding,
    )

    output_directory = Path(args.output)

    atlas_path = output_directory / "atlas.png"
    metadata_path = output_directory / "atlas.json"

    generate_atlas(
        sprites,
        packed_sprites,
        str(atlas_path),
        args.width,
        atlas_height,
    )

    generate_metadata(
        packed_sprites,
        atlas_path.name,
        args.width,
        atlas_height,
        str(metadata_path),
    )

    print(f"Atlas size: {args.width}x{atlas_height}")
    print(f"Created: {atlas_path}")
    print(f"Created: {metadata_path}")
    print("Done.")


if __name__ == "__main__":
    main()