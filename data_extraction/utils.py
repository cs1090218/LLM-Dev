import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


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


def create_new_sheet(spreadsheet_id, sheet_name):
  """Adds a new sheet"""
  creds = get_creds()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    
    # Create the new sheet in the spreadsheet
    body = {
        "requests":{
            "addSheet":{
                "properties":{
                    "title":sheet_name
                }
            }
        }
    }
    result = service.spreadsheets().batchUpdate(
       spreadsheetId=spreadsheet_id, body=body).execute()
    print (f"Created a new sheet result: {result}")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


def write_content(spreadsheet_id, range_name, values):
  """Write content to sheet"""
  creds = get_creds()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body,
        )
        .execute()
    )
    print(f"Exported content to {result.get('updatedCells')} cells.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


def read_sheet(spreadsheet_id, sheet_name):
  """Read a sheet"""
  creds = get_creds()
  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range=sheet_name)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return None

    return values
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


def format_sheet(spreadsheet_id, sheet_id):
  """Does following operations:
    1- Freeze top row
    2- Bold top row
    3- Change the width of first column to 400 pixels
  
  """
  creds = get_creds()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    
    # Create the new sheet in the spreadsheet
    body = {
        "requests": [{
            "updateSheetProperties": {                 
                "properties": {
                "sheetId": sheet_id,
                "grid_properties": { "frozen_row_count": 1 }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1
                },
                "cell": {
                    "userEnteredFormat": { "textFormat": { "bold": True } }
                },
                "fields": "userEnteredFormat(textFormat)"
            }
        },
        {
            "updateDimensionProperties": {
                "properties": {"pixelSize": 400},
                "range": {
                    "dimension": "COLUMNS",
                    "sheetId": sheet_id,
                    "startIndex": 0,
                    "endIndex": 1,
                },
                "fields": "pixelSize",
            }
        }]
    }
    result = service.spreadsheets().batchUpdate(
       spreadsheetId=spreadsheet_id, body=body).execute()
    print (f"Format sheet result: {result}")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
