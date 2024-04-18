# cs-surf-archive
cs-surf-archive.github.io

### Generating the website
- Generate credentials for Google Sheets API
- Run site_generator.py

### How generate_website.py works
- Imports get_sheet_data.py
- Stores all data from the sheet in a variable
- Calls generate_css_html, generate_overflow_html, and generate_other_html to
- - split out css, other, and overflow maps into their own pages
- - build the HTML for each page
- runs tests if TESTS_ENABLED == True
- writes to sheet if WRITE_SHEET == True

### test_drive_matches_sheet
- checks if all files in the drive have entries in the sheet
- if it doesnt, it appends mapnames with download links to end of spreadsheet
  
### test_mapname_filename_match
- ensures the map name on the sheet matches the file name on drive

### write_screenshots_to_sheet
- searches drive for screenshots, matches them with maps in the sheet based on filename, and writes the screenshot link to the sheet.

### insert_missing_maps
- searches the drive for maps that don't exist in the sheet, creates mapname only entries in the sheet, then alphabetizes the sheet.
  
### other notes
- the goal of this is to be able to generate a website, without spending all my time doing it.  The scope has grown, and the original method is showing growing pains.
- get_sheet_data.py, when called by generate_website.py, generates the token for the API
- if scopes are changed, token needs to be regenerated
- currently the only user with api access is cs-surf-archive@gmail.com
- each generate_*_html file contains a unique string appended to the end of preboiler to make a unique link line per page
- gtoken.py gets the credentials for Google API.  Delete token.json locally for it to refresh
- the 3 generate_*_html.py files are all the same except for 3 lines lol.  if I have to mess with the pages again I'll come up with a more graceful solution.
- Instead of getting sheet data multiple times, then rewriting per cell, a good rewrite would be to modify it all locally then rewrite per sheet.
- After adding a file to the drive, sheet has to be regenerated multiple times.  Don't have time to fix yet.