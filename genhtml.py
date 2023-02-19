import sheetdata
import test_mapname_filename_match

def main():
    data = sheetdata.get_data()
    collapsible_with_dl, collapsible_no_dl = create_collapsible(data)
    table_data = build_table(collapsible_with_dl, collapsible_no_dl)
    site = build_index_html(table_data)
    write_file(site)

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

    collapsible_list_dl = []
    collapsible_list_no_dl = []
    collapsed_content = []

    for map_num in range(len(data)):
        name.append([])
        if map_num != 0: # first index is always headers, so skip
            content.append([])
            name[map_num-1].append(data[map_num][0])
            for info in range(len(data[map_num])):
                if "drive.google.com" in data[map_num][info]: # build a link if it finds HTTP in the string
                    linkurl = data[map_num][info]
                    linktext = str(name[map_num-1]).strip('[]\'')
                    link = linkpre + linkurl + linkmid + linktext + linkclose
                    print(link)
                    content[map_num-1].append(bo + str(data[0][info] + bc + ":" + br + " \n" + tab + link + br + "\n"))
                else:
                    content[map_num-1].append(bo + str(data[0][info] + bc + ":" + br + " \n" + tab + data[map_num][info] + br + "\n"))
                

    for content_num in range(len(content)):
        collapsed_content.append("\n".join(content[content_num])) # join all the individual items into a single string

        if "drive.google.com" in collapsed_content[content_num]:
            collapsible_list_dl.append(pre+str(name[content_num]).strip('[]\'')+bridge+str(collapsed_content[content_num])+final)
        else:
            collapsible_list_no_dl.append(pre+str(name[content_num]).strip('[]\'')+bridge+str(collapsed_content[content_num])+final)

    return collapsible_list_dl, collapsible_list_no_dl

def build_table(collapsible_list_dl, collapsible_list_no_dl):
    tablepre = "<table>\n\t<tr>\n\t\t<th>With Download</th>\n\t\t<th>Without download</th>\n\t</tr>"
    tablemid = []
    tablepost = "\n</table>"

    tablemid.append([])
    for map in range(len(collapsible_list_dl)):
        tablemid[0].append(collapsible_list_dl[map])

    tablemid.append([])
    for map in range(len(collapsible_list_no_dl)):
        tablemid[1].append(collapsible_list_no_dl[map])

    #print(tablemid)

    tablemid = "<tr>\n\t<td>" + "".join(collapsible_list_dl) + "</td>\n\t\t<td>" + "".join(collapsible_list_no_dl) + "</td>\n</tr>"
    tablecontent = tablepre+tablemid+tablepost
    print(tablecontent)
    return tablecontent

def index_html_boilerplate():
    preboilersrc = "preboiler.html"
    postboilersrc = "postboiler.html"

    with open(preboilersrc, 'r') as file:
        preboiler = file.read()

    with open(postboilersrc, 'r') as file:
        postboiler = file.read()

    return preboiler, postboiler

def build_index_html(table_data):
    preboiler, postboiler = index_html_boilerplate()

    content = "".join(table_data)

    whole_site = preboiler + content + postboiler

    return whole_site

def write_file(whole_site):
    index = "index.html"
    with open(index, 'w') as file:
        file.write(whole_site)

if __name__ == '__main__':
    main()
    test_mapname_filename_match.check_names()
    print("all done!!")