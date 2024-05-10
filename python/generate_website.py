import get_sheet_data
import get_drive_data
import update_json_and_sheet
import config
import generate_css_html
import generate_other_html
import generate_overflow_html
import platform
import subprocess
import re

SHEET_DATA = config.get_post_processed_sheet_data_from_json()
MAP_NAME_INDEX = config.get_map_name_index()
MAP_DOWNLOAD_INDEX = config.get_map_download_index()
SCREENSHOT_INDEX = config.get_screenshot_index()
GAME_INDEX = config.get_game_index()
OVERFLOW_INDEX = config.get_overflow_index()

def create_collapsibles(data):
    collapsibles = {
        "css_dl": [],
        "css_no_dl": [],
        "other_dl": [],
        "other_no_dl": [],
        "overflow": []
    }

    column_header = data[0]  # Assuming data[0] contains column headers
    
    for row in data[1:]:
        # ok what the hell is this line?
        # one big boy list comprehension
        # it sets the content, which is one line of HTML
        # equal to the header in cell 
        # which is the pair found in each item of the list from the zip of column_header and row
        # the zip makes it so each column header is always paired with its cell
        # for reference when building the content for a collapsible.
        # it also leaves out the overflow, because overflow column is only used for sorting lists
        content = [f'<b>{header}:</b><br />&emsp;{cell}' for header, cell in zip(column_header, row) if column_header.index(header) != OVERFLOW_INDEX]
        content_html = '<br />'.join(content)
        collapsible_html = f'\n<div id="{row[MAP_NAME_INDEX]}">\n\t<button type="button" class="collapsible">{row[MAP_NAME_INDEX]}</button>\n\t<div id="{row[MAP_NAME_INDEX]}" class="content"><p>{content_html}</p></div>\n</div>'
        
        has_dl = "drive.google.com" in row[MAP_DOWNLOAD_INDEX]
        css = "CSS" in row[GAME_INDEX]
        overflow = "x" in row[OVERFLOW_INDEX]

        category = None

        # now that a collapsible element has been built for every map,
        # we need to split them out into categories
        # so they can be placed on the correct column of the correct page.
        if has_dl and css and not overflow:
            category = "css_dl"
        elif not has_dl and css and not overflow:
            category = "css_no_dl"
        elif has_dl and not css and not overflow:
            category = "other_dl"
        elif not has_dl and not css and not overflow:
            category = "other_no_dl"
        elif overflow:
            category = "overflow"
        
        if category is not None:
            collapsibles[category].append(collapsible_html)
    
    return tuple(collapsibles.values())

# lint the html, I don't like this too much since it's platform dependent
def tidy_html():
    # check if being run on linux, if so, is tidy installed? if so, run html tidy script
    if platform.system() == "Linux":
        try:
            subprocess.run(["tidy", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            tidy_script_path = "bash/tidy.sh"
            try:
                subprocess.run(["bash", tidy_script_path], check=True)
                print("HTML tidy script ran from", tidy_script_path)
            except subprocess.CalledProcessError as e:
                print(f"Error executing HTML tidy script: {e}")

        except subprocess.CalledProcessError:
            print("Tidy is not installed. Please install it before running the HTML tidy script.")

if __name__ == "__main__":
    print("==========GETTING ALL DATA FROM GOOGLE APIS==========")
    print("") # yes i know i can do \n i just like how this breaks it up visually

    get_sheet_data.get_data() # generate preprocessed json file from API
    get_drive_data.get_screenshot_items() # generate json for screenshots from api
    get_drive_data.get_map_items() # generate json for maps from api
    
    print("")
    print("==========COMBINING SHEET AND DRIVE JSONS==========")
    print("")

    update_json_and_sheet.pad_rows() # pad rows if there are empties, so it's always correct length
    update_json_and_sheet.match_screenshots_and_downloads_to_sheet() # match sheet data against screenshot and map drive json's, also format links for html
    update_json_and_sheet.add_jump_links() # build jump links for site

    print("")
    print("==========WRITING UPDATED JSON TO FILE, THEN TO SHEET==========")
    print("")

    update_json_and_sheet.write_processed_json_to_file() # write the processed json to a file
    update_json_and_sheet.write_processed_json_to_sheet() # write the processed json to sheet
    
    print("")
    print("==========BUILDING WEBSITE PAGES==========")
    print("")

    css_dl, css_no_dl, other_dl, other_no_dl, overflow = create_collapsibles(SHEET_DATA) # get variables for all collapsibles
    generate_css_html.build(css_dl, css_no_dl) # generate css HTML page (index.html)
    print("built index.html")
    generate_other_html.build(other_dl, other_no_dl) # generate other maps HTML page (other.html)
    print("built other.html")
    generate_overflow_html.build(overflow) # generate overflow maps HTML page (overflow.html)
    print("built overflow.html")