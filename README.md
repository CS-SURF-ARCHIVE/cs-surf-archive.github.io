# cs-surf-archive
cs-surf-archive.github.io

### Generating the website
- Create a credentials.json by:
1. In the Google Cloud console, go to Menu menu > IAM & Admin > Service Accounts. Go to Service Accounts.
2. Select your service account.
3. Click Keys > Add key > Create new key.
4. Select JSON, then click Create.
5. Click Close.
- Place it in the root folder
- Run generate_website.py
- Authenticate in browser to generate token.json (only cs-surf-archive@gmail.com has access)
- Watch the magic happen

### WELL HOWS IT WORK
- `config.py` contains almost all of the important variables
- `get_sheet_data.py` calls the Google API to get the Rare maps sheet in JSON format
- `get_drive_data.py` calls the Google API to items from Screenshots and Maps folders in JSON format
- `update_json_and_sheet.py` combines `sheet_data_pre_processing`, `screenshots_data.json`, and `maps_data.json`
- `set_sheet_data.py` can update either just a row or a whole sheet.  Whole sheet is only in use for now.  Row updates = too many API calls.
- This ensures the data in the drive always matches the sheet
- `generate_website.py` pulls everything together and generates HTML using `generate_css_html.py`, `generate_other_html.py`, and `generate_overflow_html.py` as templates
- `gtoken.py` is used to generate the credentials for APIs.

### todo (maybe)
- Print if map exist in drive but not sheet
- Add entry to sheet if map exist in drive but not sheet