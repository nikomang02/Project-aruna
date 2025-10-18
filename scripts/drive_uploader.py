from __future__ import print_function
import sys, os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

HOME = Path.home()
TOKEN = HOME/'credentials'/'token.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_service():
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    return build('drive', 'v3', credentials=creds)

def ensure_folder(service, name):
    q = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    res = service.files().list(q=q, fields="files(id,name)").execute()
    files = res.get('files', [])
    if files: return files[0]['id']
    meta = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    f = service.files().create(body=meta, fields='id').execute()
    return f['id']

def upload(service, path, parent_id):
    fname = os.path.basename(path)
    media = MediaFileUpload(path, resumable=False)
    meta = {'name': fname, 'parents': [parent_id]}
    f = service.files().create(body=meta, media_body=media,
                               fields='id, webViewLink').execute()
    print("Uploaded:", fname)
    print("Link:", f.get('webViewLink'))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: drive_uploader.py <file>")
        sys.exit(1)
    service = get_service()
    folder_id = ensure_folder(service, "UserLAnd Backups")
    upload(service, sys.argv[1], folder_id)
