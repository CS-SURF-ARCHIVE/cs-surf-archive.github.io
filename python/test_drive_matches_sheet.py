# maybe write something that finds maps that don't have a dl link
# and adds the dl link if it exists?
# situation occurs when we have a map name and info in the sheet
# but then add the download later
# it will not be picked up and added unless done

import os
import get_sheet_data
import gtoken
import insert_missing_maps

from googleapiclient.discovery import build

SHEET_WRITE = True # if false, does not write to sheet, test only

def get_drive_items():
    creds = gtoken.get()
    page_size = 1000
    drive_service = build('drive', 'v3', credentials=creds)
    folder_id = '1BwsG6pIsRFiCGGG7ppiLSJ0NbLv7_Xv4'
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    count = 0

    drive_items = []

    while True:
        # Call the Files:list method to retrieve a page of files and folders in the specified folder
        results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)", pageSize=page_size, pageToken=page_token).execute()

        # Print the list of files and folders in the current page
        items = results.get('files', [])
        if not items:
            print('No files or folders found.')
        else:
            for item in items:
                # Check if the item is a file (not a folder)
                if item.get('mimeType') != 'application/vnd.google-apps.folder':
                    drive_items.append(item)  # Only add files to the drive_items list
                else:
                    print("non-file found ", item)

        # Check if there are more pages of results
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    
    return drive_items

def compare_sheet_and_drive():
    drive_items = get_drive_items()
    sheet_items = get_sheet_data.get_data()

    drive_item_dict = {"mapname": [], "maplink": []}
    sheet_item_names = []

    drive_url_pre = 'https://drive.google.com/file/d/'
    drive_url_post = '/view?usp=share_link'

    for map in drive_items:
        drive_item_mapname = map['name'].rsplit('.', 1)[0].lower() #remove file extension from name
        drive_item_maplink = drive_url_pre + map['id'] + drive_url_post
        
        if ' ' in drive_item_mapname:     #for some reason " (1)" can get appended to end of files, remove it
            drive_item_mapname = drive_item_mapname.split(' ')
            drive_item_mapname = str(drive_item_mapname[0])
        
        #print(drive_item_mapname)
        drive_item_dict["mapname"].append(drive_item_mapname)
        drive_item_dict["maplink"].append(drive_item_maplink)
    
    for map in sheet_items:
        if map[0] != "name":
            sheet_item_names.append(map[0].lower())

    compared_item_names = [x for x in drive_item_dict["mapname"] if x not in sheet_item_names]
    
    return compared_item_names, drive_item_dict

def get_downloads_for_missing_maps(sheet_write):
    compared_item_names, drive_item_dict = compare_sheet_and_drive()
    missing_map_dict = {"mapname": [], "maplink": []}

    for i in range(len(drive_item_dict["mapname"])):
        if drive_item_dict["mapname"][i] in compared_item_names:
            missing_map_dict["mapname"].append(drive_item_dict["mapname"][i])
            missing_map_dict["maplink"].append(drive_item_dict["maplink"][i])
    
    for i in range(len(missing_map_dict["mapname"])):
        print("missing map", missing_map_dict["mapname"][i], missing_map_dict["maplink"][i])
    
    if sheet_write == True:
        print("write = true, writing")
        insert_missing_maps.values(missing_map_dict)
    else:
        print("write is false")

    return missing_map_dict
