import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "trips.json"


def read_trips() -> dict:
    if not DATA_FILE.exists():
        write_trips({"trips": []})
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_trips(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
