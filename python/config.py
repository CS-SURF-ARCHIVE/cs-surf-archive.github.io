# All variables in one place.  I like this.
import os
import json

#SHEET_ID = '1om84pRBMUvmVxD6ckd4u9imY9qGa1vMNPZ79WiKz9ig' # prod sheet ID
SHEET_ID = '1zlN5SnHZcB7ZyqhoZ9P32mzgxtjKmUR53n3R7H8FgnA' # test sheet ID
RANGE_NAME = "'Surf maps'" # name of the sheet, has to be in ''s because of space in name

MAPS_FOLDER_ID = '1BwsG6pIsRFiCGGG7ppiLSJ0NbLv7_Xv4'
SCREENSHOTS_FOLDER_ID = '1pHuvPJZn0UPAd4mn8y5coXBDRV3mKTFu'
MISSING_SCREENSHOT_ID = '1vS_uStVC1n2-63uDx-h5r8ZaSPbohU5W'

# 2 files for sheet json - pre and post processing
# mainly for debug purposes

DATA_FOLDER = 'data'
SHEET_DATA_FILE_PRE_PROCESSING = os.path.join(DATA_FOLDER, 'sheet_data_pre_processing.json')
SHEET_DATA_FILE_POST_PROCESSING = os.path.join(DATA_FOLDER, 'sheet_data_post_processing.json')
SCREENSHOTS_DATA_FILE_NAME = os.path.join(DATA_FOLDER, 'screenshots_data.json')
MAPS_DATA_FILE_NAME =  os.path.join(DATA_FOLDER, 'maps_data.json')

# all of these gets are because the variables may not exist at run time
# if they're defined outside of functions, they get ran as part of this code
# 
# defining them as gets allows me to dynamically call them to get their values
# instead of always running and possibly erroring out

def get_pre_processed_sheet_data_from_json():
    with open(SHEET_DATA_FILE_PRE_PROCESSING, 'r') as f:
        SHEET_DATA_PRE_PROCESSING = json.load(f)
    return SHEET_DATA_PRE_PROCESSING

def get_post_processed_sheet_data_from_json():
    with open(SHEET_DATA_FILE_POST_PROCESSING, 'r') as f:
        SHEET_DATA_POST_PROCESSING = json.load(f)
    return SHEET_DATA_POST_PROCESSING

def get_screenshot_data_from_json():
    with open(SCREENSHOTS_DATA_FILE_NAME, 'r') as f:
        SCREENSHOTS_DATA = json.load(f)
    return SCREENSHOTS_DATA

def get_map_data_from_json():
    with open(MAPS_DATA_FILE_NAME, 'r') as f:
        MAPS_DATA = json.load(f)
    return MAPS_DATA

def get_indexes_of_columns():
    indexes = {}
    sheet_data = get_pre_processed_sheet_data_from_json()
    for index, item in enumerate(sheet_data[0]):
        indexes[item] = index
    return indexes

def get_map_name_index():
    indexes = get_indexes_of_columns() 
    MAP_NAME_INDEX = indexes.get("name")
    return MAP_NAME_INDEX

def get_author_index():
    indexes = get_indexes_of_columns()
    AUTHOR_INDEX = indexes.get("author")
    return AUTHOR_INDEX

def get_release_date_index():
    indexes = get_indexes_of_columns()
    RELEASE_DATE_INDEX = indexes.get("release date")
    return RELEASE_DATE_INDEX

def get_type_index():
    indexes = get_indexes_of_columns()
    TYPE_INDEX = indexes.get("type")
    return TYPE_INDEX

def get_game_index():
    indexes = get_indexes_of_columns()
    GAME_INDEX = indexes.get("game")
    return GAME_INDEX

def get_notes_index():
    indexes = get_indexes_of_columns()
    NOTES_INDEX = indexes.get("notes")
    return NOTES_INDEX

def get_overflow_index():
    indexes = get_indexes_of_columns()
    OVERFLOW_INDEX = indexes.get("overflow")
    return OVERFLOW_INDEX

def get_screenshot_index():
    indexes = get_indexes_of_columns()
    SCREENSHOT_INDEX = indexes.get("screenshot link")
    return SCREENSHOT_INDEX

def get_map_download_index():
    indexes = get_indexes_of_columns()
    MAP_DOWNLOAD_INDEX = indexes.get("map link")
    return MAP_DOWNLOAD_INDEX

def get_jump_link_index():
    indexes = get_indexes_of_columns()
    JUMP_LINK_INDEX = indexes.get("jump link")
    return JUMP_LINK_INDEX