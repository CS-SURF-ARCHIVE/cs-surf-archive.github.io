import config
import gtoken
import hashlib
import json
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCREENSHOTS_FOLDER_ID = config.SCREENSHOTS_FOLDER_ID
SCREENSHOTS_DATA_FILE_NAME = config.SCREENSHOTS_DATA_FILE_NAME

MAPS_FOLDER_ID = config.MAPS_FOLDER_ID
MAPS_DATA_FILE_NAME = config.MAPS_DATA_FILE_NAME

IMG_FOLDER = config.IMG_FOLDER

# list of folders with their associated output file name
FOLDER_AND_FILE_NAME_PAIRS = [(SCREENSHOTS_FOLDER_ID, SCREENSHOTS_DATA_FILE_NAME), (MAPS_FOLDER_ID, MAPS_DATA_FILE_NAME)]

def get_screenshot_items():
    get_drive_items(SCREENSHOTS_FOLDER_ID, SCREENSHOTS_DATA_FILE_NAME)

def get_map_items():
    get_drive_items(MAPS_FOLDER_ID, MAPS_DATA_FILE_NAME)

def get_drive_items(folder_id, output_file_name):
    creds = gtoken.get()
    page_size = 1000
    drive_service = build('drive', 'v3', credentials=creds)
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    filenames = []

    while True:
        try:
            results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType, md5Checksum)", pageSize=page_size, pageToken=page_token).execute()

            items = results.get('files', [])
            if not items:
                print('No files or folders found.')
            else:
                for item in items:
                    if item.get('mimeType') != 'application/vnd.google-apps.folder':
                        filenames.append(item)  # Only add files to the drive_items list.  otherwise folders can show up as entries

            # Check if there are more pages of results
            page_token = results.get('nextPageToken')
            if not page_token:
                break

        except HttpError as err:
            print(err)
    
    with open(output_file_name, 'w') as json_file:
        json.dump(items, json_file)
    
    print(f'Drive data saved to {output_file_name}')


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_screenshots():
    creds = gtoken.get()
    drive_service = build('drive', 'v3', credentials=creds)
    
    
    with open(SCREENSHOTS_DATA_FILE_NAME, 'r') as json_file:
        items = json.load(json_file)
    
    print("Checking drive screenshots against local images folder, then downloading new or changed images")

    for item in items:
        file_id = item['id']
        file_name = item['name']
        mime_type = item['mimeType']
        drive_md5_checksum = item['md5Checksum']

        file_path = os.path.join(IMG_FOLDER, file_name)
        
        if os.path.exists(file_path):
            local_md5_checksum = calculate_md5(file_path)
            if drive_md5_checksum == local_md5_checksum:
                continue
            else:
                print(f"{file_name} md5 mismatch - local {local_md5_checksum} vs drive {drive_md5_checksum}")

        if 'image' in mime_type:
            request = drive_service.files().get_media(fileId=file_id)
            file_path = os.path.join(IMG_FOLDER, file_name)
            
            with open(file_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"Downloading {file_name}: {int(status.progress() * 100)}%")
    
    print('All screenshots have been processed.')

if __name__ == "__main__":
    get_screenshot_items()
    get_map_items()
    download_screenshots()