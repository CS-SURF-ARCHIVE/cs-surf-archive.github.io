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
- writes to sheet if WRITE_SHEET == True

### test_drive_matches_sheet
- checks if all files in the drive have entries in the sheet
- if it doesnt, it appends mapnames with download links to end of spreadsheet
  
### test_mapname_filename_match
- ensures the map name on the sheet matches the file name on drive
  
### other notes
- sheetdata.py, when called by genhtml.py, generates the token for the API
- if scopes are changed, token needs to be regenerated
- currently the only user with api access is cs-surf-archive@gmail.com
- html_boilerplate contains folders for both source and 1.6 pages
- pre is everything before the collapsibles get put in
- post is for everything after them
- gtoken gets the credentials for Google API.  Delete token.json for it to refresh