from datetime import datetime
from pathlib import Path
import json

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_event(event: str, detail: dict | None = None) -> None:
    """Catat event sederhana ke logs/activity.log"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {"time": ts, "event": event, "detail": detail or {}}
    line = json.dumps(payload, ensure_ascii=False)
    with open(LOG_DIR / "activity.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")
