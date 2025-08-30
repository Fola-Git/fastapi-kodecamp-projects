import json
from pathlib import Path
from .models import Note

NOTES_JSON = Path(__file__).resolve().parents[1] / "notes.json"

def backup_all(notes: list[Note]):
    data = [n.model_dump() | {"created_at": n.created_at.isoformat()} for n in notes]
    NOTES_JSON.write_text(json.dumps(data, indent=2))
