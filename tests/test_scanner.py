from pathlib import Path

from PIL import Image

from src.scanner import scan_sprites


def test_scan_sprites(tmp_path: Path) -> None:
    sprite = tmp_path / "player.png"

    image = Image.new("RGBA", (64, 32), (255, 0, 0, 255))
    image.save(sprite)

    result = scan_sprites(str(tmp_path))

    assert len(result) == 1
    assert result[0]["name"] == "player"
    assert result[0]["width"] == 64
    assert result[0]["height"] == 32


def test_non_png_files_are_ignored(tmp_path: Path) -> None:
    sprite = tmp_path / "player.png"
    text_file = tmp_path / "notes.txt"

    Image.new("RGBA", (32, 32), (255, 0, 0, 255)).save(sprite)
    text_file.write_text("not a sprite", encoding="utf-8")

    result = scan_sprites(str(tmp_path))

    assert len(result) == 1
    assert result[0]["name"] == "player"


def test_missing_directory_raises_error(tmp_path: Path) -> None:
    missing_directory = tmp_path / "missing"

    try:
        scan_sprites(str(missing_directory))
        assert False
    except FileNotFoundError:
        assert True