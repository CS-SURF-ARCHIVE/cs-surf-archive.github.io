# cs-surf-archive
cs-surf-archive.github.io

### Generating the website
- Generate credentials for Google Sheets API
- Run genhtml.py

### How genhtml.py works
- Imports sheetdata.py
- Stores all data from the sheet in a variable
- Formats it in HTML
- Opens index.html
- Pastes preboiler.html at the start
- Pastes the generated HTML from the sheet in the middle
- Pastes postboiler.html at the end

### other notes
- sheetdata.py, when called by genhtml.py, generates the token for the API
- if scopes are changed, token needs to be regenerated
- currently the only user with api access is cs-surf-archive@gmail.com