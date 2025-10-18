from pathlib import Path
from utils.logger import log_event

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def detect_tone(text: str) -> str:
    t = text.lower()
    if "?" in text:
        return "question"
    pos = any(w in t for w in ["baik", "senang", "bagus", "mantap"])
    neg = any(w in t for w in ["tidak", "buruk", "sedih", "jelek"])
    if pos and not neg:
        return "positive"
    if neg and not pos:
        return "negative"
    return "neutral"

def speak(message: str) -> str:
    """Balasan standar Aruna + log"""
    log_event("aruna_speak", {"text": message[:120]})
    return f"Aruna: {message}"

def analyze(text: str) -> dict:
    """Analisa ringan: panjang teks & tone"""
    tone = detect_tone(text)
    result = {"tone": tone, "length": len(text), "preview": text[:50]}
    log_event("analyze", result)
    return result

def save_message(text: str) -> str:
    """Simpan pesan terakhir ke data/last_message.txt"""
    (DATA_DIR / "last_message.txt").write_text(text, encoding="utf-8")
    log_event("save_message", {"saved": True, "preview": text[:50]})
    return "saved"
