import requests
import sheetdata
import re
import os
import gtoken

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


testdata = sheetdata.get_data()

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
    for row in range(len(testdata)):
        for item in range(len(testdata[row])):    
            if "drive.google.com" in testdata[row][item]:
                map_name = testdata[row][0]
                
                download_link = testdata[row][item]
                file_id = download_link.split('/')[-2]
                file_name = service.files().get(fileId=file_id, fields='name').execute()
                file_name_split = file_name['name'].rsplit('.', 1)[0].lower()

                if map_name.lower() != file_name_split:
                    print("mismatched link for", map_name, ", got", file_name_split, "download name")

if __name__ == "__main__":
    check_names()