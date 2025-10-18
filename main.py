#!/usr/bin/env python3
import sys
from core.aruna_core import speak, analyze, save_message
from utils.logger import log_event

HELP = """\
Aruna CLI
---------
Perintah:
  say "teks"          -> Aruna bicara
  analyze "teks"      -> Analisa ringan (tone, panjang)
  save "teks"         -> Simpan pesan terakhir ke data/last_message.txt
  status              -> Cek file penting & log
  help                -> Tampilkan bantuan

Contoh:
  python3 main.py say "Halo, aku baik!"
  python3 main.py analyze "Kenapa ya ini error?"
  python3 main.py save "Catatan penting hari ini"
"""

def cmd_status():
    import os
    from pathlib import Path
    ok = []
    miss = []
    for p in ["core/aruna_core.py", "utils/logger.py", "data", "logs"]:
        if Path(p).exists():
            ok.append(p)
        else:
            miss.append(p)
    print("OK   :", ", ".join(ok) if ok else "-")
    print("MISS :", ", ".join(miss) if miss else "-")
    # tampilkan 3 baris log terakhir jika ada
    logp = Path("logs/activity.log")
    if logp.exists():
        print("\nLog (tail 3):")
        lines = logp.read_text(encoding="utf-8").splitlines()[-3:]
        for ln in lines:
            print("  ", ln)
    else:
        print("\nBelum ada log.")

def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"help", "-h", "--help"}:
        print(HELP)
        return 0

    cmd = argv[1]
    arg = " ".join(argv[2:]).strip().strip("'").strip('"')

    if cmd == "say":
        if not arg:
            print("Butuh teks. Contoh: python3 main.py say \"Halo\"")
            return 1
        print(speak(arg))
        return 0

    if cmd == "analyze":
        if not arg:
            print("Butuh teks. Contoh: python3 main.py analyze \"Apa kabar?\"")
            return 1
        res = analyze(arg)
        print(res)
        return 0

    if cmd == "save":
        if not arg:
            print("Butuh teks. Contoh: python3 main.py save \"catatan...\"")
            return 1
        out = save_message(arg)
        print(out)
        return 0

    if cmd == "status":
        cmd_status()
        return 0

    print("Perintah tidak dikenal.\n")
    print(HELP)
    return 1

if __name__ == "__main__":
    log_event("cli_invoked", {"argv": sys.argv[1:]})
    raise SystemExit(main(sys.argv))
