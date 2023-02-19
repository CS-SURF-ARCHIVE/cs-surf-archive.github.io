# cs-surf-archive
cs-surf-archive.github.io

### Generating the website
- Generate credentials for Google Sheets API
- Run site_generator.py

### How site_generator.py works
- Imports sheetdata.py
- Stores all data from the sheet in a variable
- Calls css_maps_gen and other_maps_gen to 
- - split out css and source maps to their own pages
- - build the HTML
- runs tests if TESTS_ENABLED == True
  
### other notes
- sheetdata.py, when called by genhtml.py, generates the token for the API
- if scopes are changed, token needs to be regenerated
- currently the only user with api access is cs-surf-archive@gmail.com
- html_boilerplate contains folders for both source and 1.6 pages
- pre is everything before the collapsibles get put in
- post is for everything after them