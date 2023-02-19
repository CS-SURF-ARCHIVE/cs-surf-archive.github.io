import requests
import sheetdata
import re
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

testdata = sheetdata.get_data()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
            token.write(creds.to_json())

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

                if map_name.lower() not in file_name['name'].lower():
                    print("mismatched link for ", map_name, ", got ", file_name['name'], " download")
                