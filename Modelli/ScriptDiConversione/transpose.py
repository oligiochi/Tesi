import os
import MyLibrary as ml
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import scipy.io as sio

data=ml.read_json_file(r'json/NasaDataSet.json')
nuovo_path=Path("/media/ailab/RAID0/giovannioliverio/DataSet2")
print(nuovo_path)
for key in data.keys():
    for subkey in tqdm(data[key].keys(), desc="Progresso"):
        if subkey != 'Header':
            path_relativo_def=nuovo_path.joinpath(data[key][subkey])
            path_relativo_def=Path(path_relativo_def)
            genitore = path_relativo_def.parent
            if not os.path.exists(str(path_relativo_def)):
                print(f"Il file {path_relativo_def} non esiste. Passaggio saltato.")
                continue
            print(path_relativo_def)
            dataset=ml.MatToDataFrame(path_relativo_def,key='singleData',IsColpitePath=True)
            dataset.reset_index(drop=True,inplace=True)
            datasetT=dataset.transpose()
            data_dict = { 'singleData': datasetT.values }
            del dataset
            del datasetT
            sio.savemat(path_relativo_def,data_dict)
            
            
            
print("ho finito")