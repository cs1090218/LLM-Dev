import io
import os.path
import shutil

from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file ../google_token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_creds():
    m_creds = None
    if os.path.exists("../google_token.json"):
        m_creds = Credentials.from_authorized_user_file("../google_token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not m_creds or not m_creds.valid:
        if m_creds and m_creds.expired and m_creds.refresh_token:
            m_creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../google_credentials.json", SCOPES)
            m_creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../google_token.json", "w") as token:
            token.write(m_creds.to_json())
    return m_creds


def download_gfile(filename, output_path):
    creds = get_creds()
    service = build("drive", "v3", credentials=creds)
    response = service.files().list(q=f"name = '{filename}'", fields='nextPageToken, files(id, name, mimeType)').execute()
    file_id = response['files'][0]['id']

    try:
        if response['files'][0]['mimeType'].startswith('application/vnd.google-apps.'):
            print (f"Downloading Google Doc/Sheet: {filename}")
            request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
            fh = io.FileIO(output_path, mode='wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            print (f"Downloaded {filename}")
        elif response['files'][0]['mimeType'].startswith('application/pdf'):
            print (f"Downloading PDF: {filename}")
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            with open(output_path, 'wb') as f:
                shutil.copyfileobj(fh, f)
            print (f"Downloaded {filename}")
        else:
            print ("Unknown file type")
    except:
        print (f"Error downloading {filename}")
