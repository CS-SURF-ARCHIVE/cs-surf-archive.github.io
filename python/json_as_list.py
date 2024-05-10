import json

def load_file_data(file_name):
    with open(file_name, 'r') as json_file:
        sheet_data_as_list = json.load(json_file)
    return sheet_data_as_list