from __future__ import print_function

import config
import gtoken

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# PROD SHEET
SHEET_ID = config.SHEET_ID

def update_row(row_index, row_data):
    # updates a single row, based on the index
    # index 0 = a1
    update_range = "A" + str(row_index) + ":I" + str(row_index) # construct the range based on index
    creds = gtoken.get()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        update_body = {
            'values': [row_data]
        }
        
        request = service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=update_range,
            valueInputOption='USER_ENTERED',
            body=update_body
        )

        response = request.execute()
        num_cells_updated = response.get('updatedCells', 0)
        print(f'{num_cells_updated} cells updated in {update_range} in {SHEET_ID}.')

    except HttpError as err:
        print(err)

# test it on the test sheet
# data = ["a", "b", "c", "d", "E", "f", "G"]
# index = 2
# update_row(index, data)
        
def update_sheet(sheet_data):
    creds = gtoken.get()

    # explain this sorcery
    # range has to be provided in cell coordinates
    # it always starts at a1
    # end is always index of last row/last column
    # chr(ord) returns a letter for a given number, so we say add the length of the sheet_data list at the first row to a to get the letter
    # then append the length of the sheet_data list total, which is the number of rows
    update_range = "A1" + ":" + (chr(ord('a') + len(sheet_data[0]))) + str(len(sheet_data))

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Prepare the update body
        update_body = {
            'values': sheet_data
        }
        
        request = service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=update_range,  
            valueInputOption='USER_ENTERED',
            body=update_body
        )

        response = request.execute()
        num_cells_updated = response.get('updatedCells', 0)
        print(f'{num_cells_updated} cells updated in Sheet1 in {SHEET_ID}.')

    except HttpError as err:
        print(err)