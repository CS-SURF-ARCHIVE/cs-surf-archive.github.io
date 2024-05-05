from __future__ import print_function

import config

import gtoken

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SHEET_ID = config.SHEET_ID
RANGE_NAME = config.RANGE_NAME

def get_data():

    creds = gtoken.get()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

    except HttpError as err:
        print(err)

    return values

if __name__ == "__main__":
    get_data()