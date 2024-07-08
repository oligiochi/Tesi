import os
import json
import MyLibrary as ml

def convert_to_json(folder_path):
    addresses = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.mat'):
            file_path = os.path.join(folder_path, filename)
            file_name_without_extension = filename.replace('.mat', '')
            addresses[file_name_without_extension] = file_path
    sorted_dict = dict(sorted(addresses.items()))
    return sorted_dict

folder_path = r'DataSetNasa\B101\B101'  # Replace with the actual folder path
folder_path = ml.path_from_root(__file__, folder_path)
json_data = convert_to_json(folder_path)
print(json_data)
#path = ml.read_json_file('Percorsi.json')['DataSetNasa']
#print(path)

