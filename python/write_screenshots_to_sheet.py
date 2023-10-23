# maybe write something that finds maps that don't have a dl link
# and adds the dl link if it exists?
# situation occurs when we have a map name and info in the sheet
# but then add the download later
# it will not be picked up and added unless done manually

# also note that if i want to do the mapname rewrite on the sheet, to do it with this method

import os
import sheetdata
import gtoken
import sheetwriter

from googleapiclient.discovery import build

SHEET_WRITE = True # if false, does not write to sheet, test only, used for local script test only

def get_drive_items():
    creds = gtoken.get()
    page_size = 1000
    drive_service = build('drive', 'v3', credentials=creds)

    screenshots_folder_id = '1pHuvPJZn0UPAd4mn8y5coXBDRV3mKTFu'
    screenshots_query = f"'{screenshots_folder_id}' in parents and trashed = false"
    
    page_token = None
    count = 0

    screenshot_filenames = []

    while True:
        # Call the Files:list method to retrieve a page of files and folders in the specified folder
        results = drive_service.files().list(q=screenshots_query, fields="nextPageToken, files(id, name, mimeType)", pageSize=page_size, pageToken=page_token).execute()

        # Print the list of files and folders in the current page
        items = results.get('files', [])
        if not items:
            print('No files or folders found.')
        else:
            for item in items:
                # Check if the item is a file (not a folder), so only get items in root dir
                if item.get('mimeType') != 'application/vnd.google-apps.folder':
                    #print(item)
                    screenshot_filenames.append(item)  # Only add files to the drive_items list
                else:
                    print("non-file found ", item)

        # Check if there are more pages of results
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    
    return screenshot_filenames

def get_mapnames_and_screenshots():
    screenshots = get_drive_items()

    link_pre = "https://drive.google.com/uc?export=view&id="

    mapnames_and_screenshots = []

    for screenshot in screenshots:
        screenshot_link = link_pre + screenshot['id']
        mapname = screenshot['name'].replace(".png", "")
    
        mapnames_and_screenshots.append((mapname, screenshot_link))
         
    return mapnames_and_screenshots  

def generate_rows_with_screenshot():
    mapnames_and_screenshots = get_mapnames_and_screenshots()
    maps_from_sheet = sheetdata.get_data()
    missing_screenshot_image_url = "https://drive.google.com/uc?export=view&id=1E7QCI9E3WWMtfdxm4rsogNlnxYJf6G9Y"
    
    indexed_maps = list(enumerate(maps_from_sheet, start=1)) # need indexed maps to correlate with the row of the spreadsheet when writing

    for index, map_item in indexed_maps[1:]: #1: allows start from index 1
        screenshot_found = False  # Flag to indicate if a matching screenshot is found
        for screenshot in mapnames_and_screenshots:
            if screenshot[0] == map_item[0]:
                if SHEET_WRITE and map_item[7] != screenshot[1]:
                    map_item[7] = screenshot[1]
                    print("writing at index ", index, " -- ", map_item)
                    sheetwriter.update_row(index, map_item)
                elif not SHEET_WRITE:
                    map_item[7] = screenshot[1]
                    print("sheet write off, but ", index, " -- ", map_item)
                screenshot_found = True
                break

        if not screenshot_found:
            try:
                if SHEET_WRITE and map_item[7] != missing_screenshot_image_url:
                    map_item[7] = missing_screenshot_image_url
                    print("writing at index ", index, " -- ", map_item)
                    sheetwriter.update_row(index, map_item)
                elif not SHEET_WRITE:
                    map_item[7] = missing_screenshot_image_url
                    print("sheet write off, but ", index, " -- missing screenshot for ", map_item[0])
            except Exception as e:
                print("failed on ", map_item, "with length ", len(map_item))
                print(e)
                
if __name__ == "__main__":
    generate_rows_with_screenshot()

    # sheet item indexes 
    # 0 = name
    # 1 = author
    # 2 = year
    # 3 = type
    # 4 = game
    # 5 = notes
    # 6 = dl link
    # 7 = ss link

    # map item indexes
    # 0 = map name
    # 1 = embeddable screenshot link