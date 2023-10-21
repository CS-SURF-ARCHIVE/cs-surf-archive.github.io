from __future__ import print_function

import os.path
import gtoken

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# updates a single row, based on the index
# index 0 = a1

# PROD SHEET
SPREADSHEET_ID = '1om84pRBMUvmVxD6ckd4u9imY9qGa1vMNPZ79WiKz9ig'

# TEST SHEET ID
# SPREADSHEET_ID = '1EfuWG4_813Y2nCF0_7grl6b1colkZzTgpSyL8xWHkz0'

def update_row(row_index, row_data):
    update_range = "A" + str(row_index) + ":H" + str(row_index) # construct the range based on index
    creds = gtoken.get()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        update_body = {
            'values': [row_data]
        }
        
        request = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=update_range,
            valueInputOption='USER_ENTERED',
            body=update_body
        )

        response = request.execute()
        num_cells_updated = response.get('updatedCells', 0)
        print(f'{num_cells_updated} cells updated in {update_range} in {SPREADSHEET_ID}.')

    except HttpError as err:
        print(err)

# test it on the test sheet
# data = ["a", "b", "c", "d", "E", "f", "G"]
# index = 2
# update_row(index, data)