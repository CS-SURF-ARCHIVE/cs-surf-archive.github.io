import os

#SHEET_ID = '1om84pRBMUvmVxD6ckd4u9imY9qGa1vMNPZ79WiKz9ig' # prod sheet ID
SHEET_ID = '13sUolfNnFm6_Y6Z2O9DiF5_FUe7b6XCT5Q84l87b5hQ' # testgit s sheet ID
RANGE_NAME = "'Surf maps'" # name of the sheet, has to be in ''s because of space in name

MAPS_FOLDER_ID = '1BwsG6pIsRFiCGGG7ppiLSJ0NbLv7_Xv4'
SCREENSHOTS_FOLDER_ID = '1pHuvPJZn0UPAd4mn8y5coXBDRV3mKTFu'

DATA_FOLDER = 'data'
SHEET_DATA_FILE_NAME = os.path.join(DATA_FOLDER, 'sheet_data.json')
SCREENSHOTS_DATA_FILE_NAME = os.path.join(DATA_FOLDER, 'screenshots_data.json')
MAPS_DATA_FILE_NAME =  os.path.join(DATA_FOLDER, 'maps_data.json')