"""Load local public data. Run commands from any directory; no network needed."""
import json
from pathlib import Path
from settings import PROGRAMME_FILE

DATA_FOLDER = Path(__file__).resolve().parent / "data"


def load_json(filename):
    return json.loads((DATA_FOLDER / filename).read_text(encoding="utf-8"))


def load_programmes():
    """The programme list the website uses. Tests always load programmes.json directly."""
    return load_json(PROGRAMME_FILE)
