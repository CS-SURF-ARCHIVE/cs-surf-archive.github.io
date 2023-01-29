import sheetdata

def main():
    data = sheetdata.get_data()
    collapsible = create_collapsible(data)
    site = build_html(collapsible)
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

    collapsible_list = []
    collapsed_content = []

    for map_num in range(len(data)):
        name.append([])
        if map_num != 0: # first index is always headers, so skip
            content.append([])
            name[map_num-1].append(data[map_num][0])
            for info in range(len(data[map_num])):
                if "http" in data[map_num][info]:
                    linkurl = data[map_num][info]
                    linktext = str(name[map_num-1]).strip('[]\'')
                    link = linkpre + linkurl + linkmid + linktext + linkclose
                    print(link)
                    content[map_num-1].append(bo + str(data[0][info] + bc + ":" + br + " \n" + tab + link + br + "\n"))
                else:
                    content[map_num-1].append(bo + str(data[0][info] + bc + ":" + br + " \n" + tab + data[map_num][info] + br + "\n"))
                

    for content_num in range(len(content)):
        collapsed_content.append("\n".join(content[content_num]))
        collapsible_list.append(pre+str(name[content_num]).strip('[]\'')+bridge+str(collapsed_content[content_num])+final)

    return(collapsible_list)

def html_boilerplate():
    preboilersrc = "preboiler.html"
    postboilersrc = "postboiler.html"

    with open(preboilersrc, 'r') as file:
        preboiler = file.read()

    with open(postboilersrc, 'r') as file:
        postboiler = file.read()

    return preboiler, postboiler

def build_html(collapsible):
    preboiler, postboiler = html_boilerplate()

    content = "".join(collapsible)


    whole_site = preboiler + content + postboiler

    #print(whole_site)
    return whole_site

def write_file(whole_site):
    index = "index.html"
    with open(index, 'w') as file:
        file.write(whole_site)


if __name__ == '__main__':
    main()