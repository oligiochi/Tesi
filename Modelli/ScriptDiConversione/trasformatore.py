import os
import MyLibrary as ml
from pathlib import Path
from tqdm import tqdm
import pandas as pd

data=ml.read_json_file(r'json/NasaDataSet.json')
nuovo_path=Path("/media/ailab/RAID0/giovannioliverio/DataSet2")
print(nuovo_path)
for key in data.keys():
    for subkey in tqdm(data[key].keys(), desc="Progresso"):
        if subkey != 'Header':
            path_relativo_def=nuovo_path.joinpath(data[key][subkey])
            print(path_relativo_def)
            path_relativo_def=Path(path_relativo_def)
            genitore = path_relativo_def.parent
            if not os.path.exists(str(path_relativo_def)):
                print(f"Il file {path_relativo_def} non esiste. Passaggio saltato.")
                continue
            
            dataset=ml.MatToDataFrame(path_relativo_def,key='singleData',IsColpitePath=True)
            print(dataset.shape)
            print(dataset)
            
            percorso_completo=genitore / (subkey + '.csv')
            print(percorso_completo)
            dataset.to_csv(percorso_completo,index=False,sep=',',header=False)
            print("ok")
            dataset=pd.read_csv(percorso_completo,delimiter=',')
            print(dataset.shape)
            del dataset
            os.remove(path_relativo_def)
            
print("ho finito")