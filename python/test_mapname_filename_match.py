# this thing kinda sucks it was written when we were still doing
# a lot of the sheet manually.

# a better thing to do would be to just write the cells
# with the google drive link each time, like I do for test_screenshots_in_sheet.py

import config
import requests
import json_as_list
import re
import gtoken

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SHEET_DATA_FILE_NAME = config.SHEET_DATA_FILE_NAME
testdata = json_as_list.load_as_list(config.SHEET_DATA_FILE_NAME)

creds = gtoken.get()

service = build('drive', 'v3', credentials=creds)

def get_filename(url):
    response = requests.get(url)
    if response.status_code == 200:
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = re.findall('filename="(.+)"', content_disposition)
            if len(filename) > 0:
                return filename[0]
            else:
                print("Could not extract filename from Content-Disposition header.")
        else:
            print("Content-Disposition header not found.")
    else:
        print(f"Request failed with status code {response.status_code}.")
    return None

def check_names():
    i = 0
    for row in range(len(testdata)):
        if "drive.google.com" in testdata[row][6]:
            #print(i)
            i+=1
            try:
                map_name = testdata[row][0]
                download_link = testdata[row][6]
                file_id = download_link.split('/')[-2]
                file_name = service.files().get(fileId=file_id, fields='name').execute()
                file_name_split = file_name['name'].rsplit('.', 1)[0].lower()
            except:
                print("error on ", map_name)

            if map_name.lower() != file_name_split:
                print("mismatched link for", map_name, ", got", file_name_split, "download name")

if __name__ == "__main__":
    check_names()