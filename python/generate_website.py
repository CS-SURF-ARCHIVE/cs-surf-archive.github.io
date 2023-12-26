import get_sheet_data
import generate_css_html
import generate_other_html
import generate_overflow_html
import platform
import subprocess
import test_mapname_filename_match
import test_drive_matches_sheet
import write_screenshots_to_sheet

TESTS_ENABLED = False
WRITE_TO_SHEET = False

def main():
    data = get_sheet_data.get_data()
    collapsible_with_dl, collapsible_no_dl, overflow = create_collapsible(data)
    css_dl, css_no_dl, other_dl, other_no_dl = split_map_by_category(collapsible_with_dl, collapsible_no_dl)
    generate_css_html.build(css_dl, css_no_dl)
    generate_other_html.build(other_dl, other_no_dl)
    generate_overflow_html.build(overflow)

def create_collapsible(data):
    collapsible_list_dl = []
    collapsible_list_no_dl = []
    overflow_list = []

    map_name_index = 0
    link_index = 6
    img_index = 7
    overflow_index = 8

    for row in data[1:]:  # Skip the header row
        content = []
        has_dl = False
        overflow = False

        # this could be done by setting variables to each index without a second for loop and the if statements
        # but this way feels a little more readable to me
        
        for index, item in enumerate(row[0:], start=0): 
            column_header = data[0][index]

            if index == map_name_index:
                map_name = item

            elif index == overflow_index and item is not None:
                overflow = True

            elif index == link_index and "drive.google.com" in item and overflow == False:
                # Handle links for the specified index
                drive_link_from_sheet = item
                site_link = f'<a href="{drive_link_from_sheet}">{map_name}.zip</a>' # don't feel like calling drive api every time to get file type.  it's always zip for
                content.append(f'<b>{column_header}:</b><br />&emsp;{site_link}') 
                has_dl = True
            
            elif index == link_index and "drive.google.com" not in item and overflow == False:
                has_dl = False

            elif index == img_index and "drive.google.com" in item:
                # Handle images with missing or error alt text for the specified index
                img_alt = f'{map_name}'
                img_link = f'<img src="{item}" alt="{img_alt}" class="ImgThumbnail" loading="lazy">'
                content.append(f'<b>screenshot:</b><br />&emsp;{img_link}')
                site_link = (f'<b>site link:</b><br />&emsp;<a href="#{map_name}">{map_name}</a>')
                content.append(site_link) # screnshot is last thing processed, and we want the site link after that.

            elif index == overflow_index and item is not None:
                pass

            else:
                # Handle regular content
                content.append(f'<b>{column_header}:</b><br />&emsp;{item}') # noted above, data[0] = column header name

        content_html = '<br />'.join(content)
        collapsible_html = f'\n<div id="{map_name}">\n\t<button type="button" class="collapsible">{map_name}</button>\n\t<div id="{map_name}" class="content"><p>{content_html}</p></div>\n</div>'
        # This line is a little absurd
        # JS found in collapsible_handler.js utilizes the nested divs with the same name
        # if a jump link is followed to a matching map name, the JS expands that collapsible.

        if has_dl and not overflow:
            collapsible_list_dl.append(collapsible_html)

        elif not has_dl and not overflow:
            collapsible_list_no_dl.append(collapsible_html)

        elif overflow:
            overflow_list.append(collapsible_html)

    return collapsible_list_dl, collapsible_list_no_dl, overflow_list

def split_map_by_category(collapsible_list_dl, collapsible_list_no_dl):
    collapsible_list_css_dl = []
    collapsible_list_css_no_dl = []
    collapsible_list_1p6_dl = []
    collapsible_list_1p6_no_dl = []

    for item in range(len(collapsible_list_dl)):
        if "CSS" in collapsible_list_dl[item]:
            collapsible_list_css_dl.append(collapsible_list_dl[item])
        else:
            collapsible_list_1p6_dl.append(collapsible_list_dl[item])
    
    for item in range(len(collapsible_list_no_dl)):
        if "CSS" in collapsible_list_no_dl[item]:
            collapsible_list_css_no_dl.append(collapsible_list_no_dl[item])
        else:
            collapsible_list_1p6_no_dl.append(collapsible_list_no_dl[item])
    
    return collapsible_list_css_dl, collapsible_list_css_no_dl, collapsible_list_1p6_dl, collapsible_list_1p6_no_dl

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
    else:
        print("This script is intended to run on Linux.")

if __name__ == '__main__':
    if WRITE_TO_SHEET == True:
        print("Writing links to all screenshots in drive to sheet")
        write_screenshots_to_sheet.generate_rows_with_screenshot()
    main()
    if TESTS_ENABLED == True:
        print("Testing if all drive files have sheet entry")
        test_drive_matches_sheet.get_downloads_for_missing_maps(WRITE_TO_SHEET) # this is confusing, maybe split into a test and a write
        print("Testing if all mapnames match filenames for downloads")
        test_mapname_filename_match.check_names()
        print("all done with tests!!")
    else:
        print("no tests, all done")
    print("tidying html")
    tidy_html()