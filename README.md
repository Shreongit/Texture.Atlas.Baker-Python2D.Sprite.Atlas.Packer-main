# Texture Atlas Baker

A standalone Python CLI tool for automatically combining multiple 2D PNG sprites into a compact texture atlas and generating JSON metadata for locating each sprite.

## Features

- PNG sprite discovery
- Automatic sprite dimension detection
- Next-Fit Decreasing Height (NFDH) packing
- Configurable atlas width
- Configurable sprite padding
- RGBA texture atlas generation
- JSON metadata generation
- Custom input and output directories
- CLI argument validation
- Automated unit and integration test

## Tech Stack

- **Language:** Python
- **Image Processing:** Pillow
- **Testing:** Pytest
- **Data Format:** JSON
- **Version Control:** Git

## Project Structure

```text
texture-atlas-baker-python/
├── assets/
│   └── sprites/
│       └── *.png
├── output/
│   ├── atlas.png
│   └── atlas.json
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── scanner.py
│   ├── packer.py
│   ├── atlas.py
│   └── metadata.py
├── tests/
│   ├── __init__.py
│   ├── test_atlas.py
│   ├── test_integration.py
│   ├── test_metadata.py
│   ├── test_packer.py
│   └── test_scanner.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place PNG sprites inside:

```text
assets/sprites/
```

Run with the default configuration:

```bash
python -m src.main
```

### Custom Configuration

The CLI supports custom input/output directories, atlas width, and padding:

```bash
python -m src.main --input assets/sprites --output output --width 1024 --padding 4
```

### CLI Options

| Option | Description | Default |
|---|---|---:|
| `--input` | Directory containing PNG sprites | `assets/sprites` |
| `--output` | Directory for generated files | `output` |
| `--width` | Atlas width in pixels | `2048` |
| `--padding` | Padding between sprites in pixels | `2` |

The tool validates the width, padding, and input directory before processing.

## Processing Pipeline

```text
PNG Sprite Directory
        │
        ▼
   Sprite Scanner
        │
        ▼
 Sprite Dimensions
        │
        ▼
Height-Based Sorting
        │
        ▼
NFDH Packing Algorithm
        │
        ├───────────────┐
        ▼               ▼
 Atlas Generator   Metadata Generator
        │               │
        ▼               ▼
   atlas.png        atlas.json
```

## Packing Algorithm

The project uses the **Next-Fit Decreasing Height (NFDH)** heuristic.

Sprites are:

1. Sorted by height in descending order.
2. Placed from left to right on the current row.
3. Moved to a new row when the next sprite does not fit.
4. Assigned final `x`, `y`, `width`, and `height` values.

The algorithm is heuristic-based rather than an optimal bin-packing solver, making it simple and fast for a lightweight asset pipeline.

## Generated Metadata

The generated `atlas.json` contains the atlas dimensions and the location of every sprite:

```json
{
    "image": "atlas.png",
    "width": 1024,
    "height": 4287,
    "sprites": {
        "player": {
            "x": 4,
            "y": 4,
            "width": 64,
            "height": 64
        }
    }
}
```

A game renderer can use these coordinates to extract individual sprites from the atlas instead of loading every source image separately.

## Testing

Run the complete test suite:

```bash
pytest
```

The project currently includes tests covering:

- Sprite scanning
- PNG filtering
- Missing input directories
- Height-based sorting
- Atlas boundary checks
- Invalid atlas widths
- Invalid padding
- Sprites wider than the atlas
- JSON metadata generation
- Multiple sprite metadata entries
- Atlas image generation
- Complete end-to-end pipeline

Current test status:

```text
12 passed
```

## Example

```bash
python -m src.main --input assets/sprites --output output --width 1024 --padding 4
```

Example output:

```text
Texture Atlas Baker
--------------------
Found 7 sprites.
Atlas size: 1024x4287
Created: output\atlas.png
Created: output\atlas.json
Done.
```

## Output

Generated files:

```text
output/
├── atlas.png
└── atlas.json
```

`atlas.png` contains all packed sprites.

`atlas.json` contains the coordinates and dimensions required to locate each sprite.

## License

MIT License
