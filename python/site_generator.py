import sheetdata as sheetdata
import css_maps_gen
import other_maps_gen
import test_mapname_filename_match
import test_drive_matches_sheet
import write_screenshots_to_sheet

TESTS_ENABLED = True
WRITE_TO_SHEET = True

def main():
    data = sheetdata.get_data()
    collapsible_with_dl, collapsible_no_dl = create_collapsible(data)
    css_dl, css_no_dl, other_dl, other_no_dl, = split_map_by_game(collapsible_with_dl, collapsible_no_dl)
    css_maps_gen.build(css_dl, css_no_dl)
    other_maps_gen.build(other_dl, other_no_dl)

def create_collapsible(data):
    collapsible_list_dl = []
    collapsible_list_no_dl = []

    link_index = 6
    img_index = 7

    for row in data[1:]:  # Skip the header row
        name = row[0]
        content = []

        for index, item in enumerate(row[1:], start=1):
            if index == link_index and "drive.google.com" in item:
                # Handle links for the specified index
                link = f'<a href="{item}">{name}</a>'
                content.append(f'<b>{data[0][index]}:</b><br />&emsp;{link}')
            elif index == img_index and "drive.google.com" in item:
                # Handle images with missing or error alt text for the specified index
                img_alt = f'{name} (img missing or error)'
                img_link = f'<a href="{item}"><img src="{item}" alt="{img_alt}" width="100%" loading="lazy"></a>'
                content.append(f'<b>{data[0][index]}:</b><br />&emsp;{img_link}')
            else:
                # Handle regular content
                content.append(f'<b>{data[0][index]}:</b><br />&emsp;{item}')

        content_html = '<br />'.join(content)
        collapsible_html = f'<button type="button" class="collapsible">{name}</button>\n<div class="content"><p>{content_html}</p></div>'

        if "drive.google.com" in content_html:
            collapsible_list_dl.append(collapsible_html)
        else:
            collapsible_list_no_dl.append(collapsible_html)

    return collapsible_list_dl, collapsible_list_no_dl

def create_imglink(mapname, image_link):
    pass

def split_map_by_game(collapsible_list_dl, collapsible_list_no_dl):
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