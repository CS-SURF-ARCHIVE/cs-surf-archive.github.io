import config
import gtoken
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCREENSHOTS_FOLDER_ID = config.SCREENSHOTS_FOLDER_ID
SCREENSHOTS_DATA_FILE_NAME = config.SCREENSHOTS_DATA_FILE_NAME

MAPS_FOLDER_ID = config.MAPS_FOLDER_ID
MAPS_DATA_FILE_NAME = config.MAPS_DATA_FILE_NAME

# list of folders with their associated output file name
FOLDER_AND_FILE_NAME_PAIRS = [(SCREENSHOTS_FOLDER_ID, SCREENSHOTS_DATA_FILE_NAME), (MAPS_FOLDER_ID, MAPS_DATA_FILE_NAME)]

def get_drive_items(folder_id, output_file_name):
    creds = gtoken.get()
    page_size = 1000
    drive_service = build('drive', 'v3', credentials=creds)
    screenshots_query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    screenshot_filenames = []

    while True:
        try:
            results = drive_service.files().list(q=screenshots_query, fields="nextPageToken, files(id, name, mimeType)", pageSize=page_size, pageToken=page_token).execute()

            items = results.get('files', [])
            if not items:
                print('No files or folders found.')
            else:
                for item in items:
                    if item.get('mimeType') != 'application/vnd.google-apps.folder':
                        screenshot_filenames.append(item)  # Only add files to the drive_items list
                    else:
                        print("non-file found ", item)

            # Check if there are more pages of results
            page_token = results.get('nextPageToken')
            if not page_token:
                break

        except HttpError as err:
            print(err)
    
    with open(output_file_name, 'w') as json_file:
        json.dump(items, json_file)
    
    print(f'Data saved to {output_file_name}')

if __name__ == "__main__":
    for folder_id, output_file_name in FOLDER_AND_FILE_NAME_PAIRS:
        get_drive_items(folder_id, output_file_name)