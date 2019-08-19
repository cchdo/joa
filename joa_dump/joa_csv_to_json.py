import json
import csv

output = {}


with open('query_result.csv', 'r') as f:
    reid_files = csv.DictReader(f)
    for row in reid_files:
        for key in row:
            if row[key] == "NULL":
                row[key] = None
            if row[key] == "South-Western\xa0":
                row[key] = "South-Western"
        if row['file_name'] in output:
            if row['basin_name'] not in output[row['file_name']]['basin_name']:
                output[row['file_name']]['basin_name'].append(row['basin_name'])
            if row['sub_basin_name'] not in output[row['file_name']]['sub_basin_name']:
                output[row['file_name']]['sub_basin_name'].append(row['sub_basin_name'])
        else:
            row['basin_name'] = [row['basin_name']]
            row['sub_basin_name'] = [row['sub_basin_name']]
            output[row['file_name']] = row

out_list = []
for key in output:
    out_list.append(output[key])

with open('joa_files.json', 'w') as f:
    json.dump(out_list, f, indent=1)
