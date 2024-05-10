# gets all of the data from the sheet and writes it to sheet_data.json
# modifications should be done to this local file instead of the sheet, to cut down on api calls

import config
import gtoken
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SHEET_ID = config.SHEET_ID
RANGE_NAME = config.RANGE_NAME
SHEET_DATA_FILE_PRE_PROCESSING = config.SHEET_DATA_FILE_PRE_PROCESSING

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

    with open(SHEET_DATA_FILE_PRE_PROCESSING, 'w') as json_file:
        json.dump(values, json_file)

    print(f'Sheet data saved to {SHEET_DATA_FILE_PRE_PROCESSING}')

if __name__ == "__main__":
    get_data()