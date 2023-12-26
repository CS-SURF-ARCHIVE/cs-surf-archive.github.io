def build_table_overflow(overflow_list):
    tablepre = "<table>\n\t<tr>\n\t\t<th>With Download</th>\n\t\t<th>Without download</th>\n\t</tr>"
    tablemid = []
    tablepost = "\n</table>"

    tablemid.append([])
    for map in range(len(overflow_list)):
        tablemid[0].append(overflow_list[map])


    tablemid = "<tr>\n\t<td>" + "".join(overflow_list) + "\n</tr>"
    tablecontent = tablepre+tablemid+tablepost
    return tablecontent

def overflow_html_boilerplate():
    preboilersrc = "html_boilerplate/pre.html"
    postboilersrc = "html_boilerplate/post.html"
    overflow_end_boiler = '<h3><a href=\"index.html\">Source Maps</a>&emsp;&emsp;<a href=\"other.html\">CS 1.6 or Unknown Maps</a>&emsp;&emsp;Overflow Maps</h3>'
    
    with open(preboilersrc, 'r') as file:
        preboiler = file.read() + overflow_end_boiler

    with open(postboilersrc, 'r') as file:
        postboiler = file.read()

    return preboiler, postboiler

def build_overflow_html(table_data):
    preboiler, postboiler = overflow_html_boilerplate()

    content = "".join(table_data)

    html = preboiler + content + postboiler

    return html

def write_file(html):
    site = "overflow.html"
    with open(site, 'w') as file:
        file.write(html)

def build(overflow):
    table_content = build_table_overflow(overflow)
    html = build_overflow_html(table_content)
    write_file(html)