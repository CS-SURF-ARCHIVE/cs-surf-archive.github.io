def build_table_other(collapsible_list_other_dl, collapsible_list_other_no_dl):
    tablepre = "<table>\n\t<tr>\n\t\t<th>With Download</th>\n\t\t<th>Without download</th>\n\t</tr>"
    tablemid = []
    tablepost = "\n</table>"

    tablemid.append([])
    for map in range(len(collapsible_list_other_dl)):
        tablemid[0].append(collapsible_list_other_dl[map])

    tablemid.append([])
    for map in range(len(collapsible_list_other_no_dl)):
        tablemid[1].append(collapsible_list_other_no_dl[map])


    tablemid = "<tr>\n\t<td>" + "".join(collapsible_list_other_dl) + "</td>\n\t\t<td>" + "".join(collapsible_list_other_no_dl) + "</td>\n</tr>"
    tablecontent = tablepre+tablemid+tablepost
    return tablecontent

def other_html_boilerplate():
    preboilersrc = "html_boilerplate/other/other_pre.html"
    postboilersrc = "html_boilerplate/other/other_post.html"

    with open(preboilersrc, 'r') as file:
        preboiler = file.read()

    with open(postboilersrc, 'r') as file:
        postboiler = file.read()

    return preboiler, postboiler

def build_other_html(table_data):
    preboiler, postboiler = other_html_boilerplate()

    content = "".join(table_data)

    html = preboiler + content + postboiler

    return html

def write_file(html):
    site = "other.html"
    with open(site, 'w') as file:
        file.write(html)

def build(collapsible_list_other_dl, collapsible_list_other_no_dl):
    table_content = build_table_other(collapsible_list_other_dl, collapsible_list_other_no_dl)
    html = build_other_html(table_content)
    write_file(html)
