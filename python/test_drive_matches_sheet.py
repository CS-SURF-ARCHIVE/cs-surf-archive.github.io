# maybe write something that finds maps that don't have a dl link
# and adds the dl link if it exists?
# situation occurs when we have a map name and info in the sheet
# but then add the download later
# it will not be picked up and added unless done

import config
import json_as_list
import write_missing_maps_to_sheet

from python.json_as_list import load_as_list
from googleapiclient.discovery import build

DRIVE_FOLDER_ID = config.DRIVE_DRIVE_FOLDER_ID
SHEET_DATA_FILE_NAME = config.SHEET_DATA_FILE_NAME

def compare_sheet_and_drive():
    drive_items = get_drive_items()
    sheet_items = json_as_list.load_file_data(SHEET_DATA_FILE_NAME)

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
        write_missing_maps_to_sheet.values(missing_map_dict)
    else:
        print("write is false")

    return missing_map_dict
