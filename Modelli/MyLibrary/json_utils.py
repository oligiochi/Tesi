import json
import os
from . import file_utils as fu
#import tensorflow as tf
# Imposta la directory di lavoro al percorso dello script
#root=fu.find_project_root(os.path.dirname(__file__))
json_path="Percorsi.json"
def read_json_file(filename):
    filename=fu.path_from_root(__file__,filename)
    with open(filename, 'r') as f:
        return json.load(f)

def write_json_file(filename, data,sort_keys=False):
    filename=fu.path_from_root(__file__,filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=sort_keys)
        
def modelTojson(model):
    m=model.to_json()
    m=json.loads(m)
    return m
# Now you can access data from the JSON object
data=read_json_file(json_path)
pathDataSet=data['DataSet']
pathsensoriDataSet=data['SensoriInfo']
pathSVN=data['SVNjson']
pathRNL=data['ReteNeuralejson']
#pathB101=data['B101']
dataSVN=read_json_file(pathSVN)
dataRNL=read_json_file(pathRNL)
#dataB101=read_json_file(pathB101)