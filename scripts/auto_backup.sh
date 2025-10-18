#!/usr/bin/env bash
set -e

# Semua kerjaan di dalam Linux HOME agar tidak memicu SAF
BACKUP_DIR="$HOME/backup"
mkdir -p "$BACKUP_DIR"

TIMESTAMP="$(date +'%Y-%m-%d_%H-%M')"
ARCHIVE="$BACKUP_DIR/userland_${TIMESTAMP}.zip"
LOG="$BACKUP_DIR/backup.log"

# Path aman untuk cron
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

echo "[$(date +'%F %T')] Start backup..." | tee -a "$LOG"

# Buat ZIP dari HOME, exclude folder backup sendiri biar gak recursive
cd "$HOME"
zip -r "$ARCHIVE" . -x "backup/*" >/dev/null

echo "[$(date +'%F %T')] Archive made: $ARCHIVE" | tee -a "$LOG"

# Upload ke Google Drive (pakai script Python kamu)
python3 "$HOME/drive_uploader.py" "$ARCHIVE" >>"$LOG" 2>&1

echo "[$(date +'%F %T')] Upload done" | tee -a "$LOG"

# OPTIONAL: hapus arsip lokal setelah sukses upload supaya hemat ruang
# rm -f "$ARCHIVE"

echo "[$(date +'%F %T')] OK" | tee -a "$LOG"
