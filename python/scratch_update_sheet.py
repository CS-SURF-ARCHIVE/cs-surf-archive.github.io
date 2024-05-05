import get_sheet_data
import sheet_writer

sheet_data = get_sheet_data.get_data()

row_num = 0

for row_index, row in enumerate(sheet_data):
    for cell_index, cell in enumerate(row):
        if cell_index == 7:
            row[cell_index] = 'test full'
            print(row[cell_index])

update_range = "A1" + ":" + (chr(ord('a') + len(sheet_data[1]))) + str(len(sheet_data))
print(update_range)


sheet_writer.update_sheet(sheet_data)