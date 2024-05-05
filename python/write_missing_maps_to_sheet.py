from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gtoken

# replace with your sheet ID
SHEET_ID = '1om84pRBMUvmVxD6ckd4u9imY9qGa1vMNPZ79WiKz9ig'

# replace with your range
RANGE_NAME = "'Surf maps'"

# load the credentials from file
credentials  = gtoken.get()
service = build('sheets', 'v4', credentials=credentials)


def values(missing_map_dict):
    insert_values = []
    # replace with your values
    for i in range(len(missing_map_dict["mapname"])):
        insert_values.append([])
        insert_values[i] = (missing_map_dict["mapname"][i], "", "", "", "", "", missing_map_dict["maplink"][i])

    # build the update request
    update_body = {
        'values': insert_values
    }
    request = service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=RANGE_NAME,
        valueInputOption='USER_ENTERED',
        body=update_body,
        insertDataOption='INSERT_ROWS',
        includeValuesInResponse=True,
        responseValueRenderOption='FORMATTED_VALUE'
    )

    # execute the request and handle any errors
    try:
        response = request.execute()
        num_cells_updated = response.get('updates', {}).get('updatedCells', 0)
        print(f'{num_cells_updated} cells appended to {RANGE_NAME} in {SHEET_ID}.')

        # Use row 1 as header and sort column A alphabetically
        sort_range = f'{RANGE_NAME}A1:A'
        sort_request_body = {
            "sortRange": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 1,
                    "endRowIndex": 1000,
                    "startColumnIndex": 0,
                    "endColumnIndex": 7
                },
                "sortSpecs": [
                    {
                        "dimensionIndex": 0,
                        "sortOrder": "ASCENDING"
                    }
                ]
            }
        }
        sort_request = service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={
            "requests": [
                {
                    "sortRange": sort_request_body["sortRange"]
                }
            ]
        })
        sort_response = sort_request.execute()
        print(f'Column A sorted alphabetically')
    except HttpError as error:
        print(f'An error occurred: {error}')