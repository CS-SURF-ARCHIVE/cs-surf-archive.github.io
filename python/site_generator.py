import sheetdata as sheetdata
import css_maps_gen as css_maps_gen
import other_maps_gen as other_maps_gen
import test_mapname_filename_match
import test_drive_matches_sheet
import test_screenshots_in_sheet

TESTS_ENABLED = True
WRITE_TO_SHEET = True

def main():
    data = sheetdata.get_data()
    collapsible_with_dl, collapsible_no_dl = create_collapsible(data)
    css_dl, css_no_dl, other_dl, other_no_dl, = split_map_by_game(collapsible_with_dl, collapsible_no_dl)
    css_maps_gen.build(css_dl, css_no_dl)
    other_maps_gen.build(other_dl, other_no_dl)


def create_collapsible(data):
    pre = "<button type=\"button\" class=\"collapsible\">"
    name = []
    bridge = "</button>\n<div class=\"content\">\n  <p>"
    content = []
    final = "</p>\n</div>"
    br = " <br />"
    tab = " &emsp; "
    bo = "<b>"
    bc = "</b>"

    linkpre = "<a href=\""
    linkurl = ""
    linkmid = "\"> "
    linktext = ""
    linkclose = "</a>"
    link = ""

    imgpre = "<img src=\""
    imgmid = "\" alt=\""
    imgclose = "\" width=\"100%\" loading=\"lazy\">"


    collapsible_list_dl = []
    collapsible_list_no_dl = []
    collapsed_content = []

    mapname_index = 1
    link_index = 6
    img_index = 7

    for map_num in range(len(data)):  #rewrite this link crap so it's not looking at the entire row for the link, but the specific index, that way i can build embed in too
        name.append([])
        if map_num != 0: # first index is always headers, so skip
            content.append([])
            name[map_num-1].append(data[map_num][0])
            for info in range(len(data[map_num])):
                if info == link_index:
                    if "drive.google.com" in data[map_num][link_index]: # build a link if it finds HTTP in the string
                        linkurl = data[map_num][link_index]
                        linktext = str(name[map_num-1]).strip('[]\'')
                        link = linkpre + linkurl + linkmid + linktext + linkclose
                        #print(str(data[0][7])) #data[0] = header, data[1] = content
                        data[map_num][link_index]=link
                        print(data[map_num][link_index])
                
                if info == img_index:
                    if "drive.google.com" in data[map_num][img_index]:
                        imgurl = data[map_num][img_index]
                        mapname = data[map_num][mapname_index]
                        imgalt = mapname + " (img missing or error)"
                        imglink = linkpre + imgurl + linkmid + "\n\t" + imgpre + imgurl + imgmid + imgalt + imgclose + "\n" + linkclose

                        data[map_num][img_index]=imglink

                content[map_num-1].append(bo + str(data[0][info] + bc + ":" + br + " \n" + tab + data[map_num][info] + br + "\n"))
                    #print(content[map_num-1])
                #print(content[map_num-1])
    for content_num in range(len(content)): # a problem existst that both lists already contain generated html
        collapsed_content.append("\n".join(content[content_num])) # join all the individual items into a single string
        if "drive.google.com" in collapsed_content[content_num]:
            collapsible_list_dl.append(pre+str(name[content_num]).strip('[]\'')+bridge+str(collapsed_content[content_num])+final)
        else:
            collapsible_list_no_dl.append(pre+str(name[content_num]).strip('[]\'')+bridge+str(collapsed_content[content_num])+final)

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
        test_screenshots_in_sheet.generate_rows_with_screenshot()
    main()
    if TESTS_ENABLED == True:
        print("Writing links to all screenshots in drive to sheet")
        test_screenshots_in_sheet.generate_rows_with_screenshot()
        print("Testing if all drive files have sheet entry")
        test_drive_matches_sheet.get_downloads_for_missing_maps(WRITE_TO_SHEET)
        print("Testing if all mapnames match filenames for downloads")
        test_mapname_filename_match.check_names()
        print("all done with tests!!")
    else:
        print("no tests, all done")