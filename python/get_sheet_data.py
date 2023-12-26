from __future__ import print_function

import os.path
import gtoken

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



SAMPLE_SPREADSHEET_ID = '1om84pRBMUvmVxD6ckd4u9imY9qGa1vMNPZ79WiKz9ig'
SAMPLE_RANGE_NAME = "'Surf maps'" # name of the sheet, has to be in 's because of space

def get_data():

    creds = gtoken.get()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

    except HttpError as err:
        print(err)
        
    return values

if __name__ == "__main__":
    get_data()