import json
import config
import os
import set_sheet_data

# variables set strictly for visibility and readability

MISSING_SCREENSHOT_ID = config.MISSING_SCREENSHOT_ID

SHEET_DATA = config.get_pre_processed_sheet_data_from_json()
SCREENSHOTS_DATA_LOCAL = config.get_screenshot_data_from_local()
MAPS_DATA = config.get_map_data_from_json()

MAP_NAME_INDEX = config.get_map_name_index()
SCREENSHOT_INDEX = config.get_screenshot_index()
MAP_DOWNLOAD_INDEX = config.get_map_download_index()
JUMP_LINK_INDEX = config.get_jump_link_index()

IMG_FOLDER = config.IMG_FOLDER

SHEET_DATA_FILE_POST_PROCESSING = config.SHEET_DATA_FILE_POST_PROCESSING

# if a sheet item doesn't have a download id or screenshot id, it won't have as many items in its entry as the header column
# so the indexes we got above will be pointing to indexes that don't exist in the item for that map's json
# so we gotta pad it with empty values, so it can write.

def pad_rows():
    max_len = len(SHEET_DATA[0])

    for row in SHEET_DATA[1:]:
        diff = max_len - len(row)
        if diff > 0:
            row += [""] * diff
    print("pad_rows function updated sheet with padded rows")

# simple helper to strip .jpg or .bsp or .png or whatever else after the . in an id from json
# also i have to put this stupid handler in there in case there's 2 dots.
def split_filename_from_extension(filename):
    filename = os.path.splitext(filename)[0]
    return filename

def build_formatted_map_link_from_id(map_id, map_name):
    # builds the map link as the website expects it fom the id
    drive_link = f"https://drive.google.com/file/d/{map_id}/view?usp=share_link"
    formatted_site_link = f'<a href="{drive_link}">{map_name}.zip</a>' # don't feel like calling drive api every time to get file type.  it's always zip for downloads
    return formatted_site_link

def build_formatted_screenshot_link_from_id(map_name, screenshot_file_name):
    # builds the screenshot link as the website expects it from the id  
    img_alt = f'{map_name}'
    formatted_screenshot_link = f'<img src="{IMG_FOLDER}/{screenshot_file_name}" alt="{img_alt}" class="ImgThumbnail" loading="lazy">'
    return formatted_screenshot_link

def build_formatted_jump_link(map_name):
    # builds the jump link as the website expects it from the map name
    formatted_jump_link = (f'<a href="#{map_name}">{map_name}</a>')
    return formatted_jump_link

def match_screenshots_and_downloads_to_sheet():
    maps_with_download_but_no_screenshot =[]

    for item in SHEET_DATA[1:]:
        map_name_from_sheet = item[MAP_NAME_INDEX]
        
        # Search for a match in SCREENSHOTS_DATA
        for screenshot_file_name in SCREENSHOTS_DATA_LOCAL:
            # screenshot_name_no_extension effectively becomes map_name
            screenshot_name_no_extension = split_filename_from_extension(screenshot_file_name) 
            if str(screenshot_name_no_extension.lower()) == map_name_from_sheet.lower():
                item[SCREENSHOT_INDEX] = build_formatted_screenshot_link_from_id(screenshot_name_no_extension, screenshot_file_name)
                break

        # Search for a match in MAPS_DATA
        for map_item in MAPS_DATA:
            map_name_from_drive = split_filename_from_extension(map_item['name'])
            
            if map_name_from_drive.lower() == map_name_from_sheet.lower():
                item[MAP_DOWNLOAD_INDEX] = build_formatted_map_link_from_id(map_item['id'], map_name_from_sheet)
                break

        # now that both maps and screenshots have been written,
        # look for entries of maps that have downloads but no screenshots
        # and add the missing screenshot image for both
            
        # LETS EXPLAIN THIS ONE A BIT
        # if the map download index has drive.google.com in it (meaning it has a link)
        # and the screenshot index doesn't have "img" in it (meaning there is no link)
        #   this can occur if a map is manually added
        # or the missing map ID is in the screenshot index (meaning there's already a missing screenshot link)
        #   this can occur if the sheet update code has been run
        # then we know we have a map with a download but no screenshot
        # so print about it and overwrite the cell with the missing image link
            
        if "drive.google.com" in item[MAP_DOWNLOAD_INDEX] and ("img" not in item[SCREENSHOT_INDEX] or MISSING_SCREENSHOT_ID in item[SCREENSHOT_INDEX]):
            item[SCREENSHOT_INDEX] = build_formatted_screenshot_link_from_id(MISSING_SCREENSHOT_ID, item[MAP_NAME_INDEX])
            maps_with_download_but_no_screenshot.append(item[MAP_NAME_INDEX])
        elif "drive.google.com" not in item[MAP_DOWNLOAD_INDEX]:
            item[SCREENSHOT_INDEX] = build_formatted_screenshot_link_from_id(MISSING_SCREENSHOT_ID, MISSING_SCREENSHOT_ID) # just pass it twice since it's the image name and alt text

    print("maps with download but no screenshot: ", maps_with_download_but_no_screenshot)
    print(len(maps_with_download_but_no_screenshot), "total maps with download but no screenshot")

def add_jump_links():
    for item in SHEET_DATA[1:]:
        item[JUMP_LINK_INDEX] = build_formatted_jump_link(item[MAP_NAME_INDEX]) # use the map name to build a jump link
    print("Added jump links")

def write_processed_json_to_file():
    with open(SHEET_DATA_FILE_POST_PROCESSING, 'w') as f:
        json.dump(SHEET_DATA, f, indent=4)

    print("Data updated and saved to", SHEET_DATA_FILE_POST_PROCESSING)

def write_processed_json_to_sheet():
    set_sheet_data.update_sheet(SHEET_DATA)

if __name__ == "__main__":
    pad_rows()
    match_screenshots_and_downloads_to_sheet()
    add_jump_links()
    write_processed_json_to_file()
    write_processed_json_to_sheet()
