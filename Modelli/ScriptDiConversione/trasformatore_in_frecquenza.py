import os
import sys
# Aggiungi il percorso della directory che contiene MyLibrary al percorso di ricerca di Python
my_library_path = os.path.join(os.path.dirname(__file__), '..', '..', 'MyLibrary')
sys.path.append(my_library_path)
import MyLibrary as ml
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import scipy.io as sio

data=ml.read_json_file(r'json/NasaDataSetPath.json')
nuovo_path=Path("/media/ailab/RAID0/giovannioliverio/DataSet2")

for key in data.keys():
    jsoncorrente=ml.read_json_file(data[key])
    for subkey in tqdm(jsoncorrente.keys(), desc="Progresso"):
        path_relativo_def=Path(jsoncorrente[subkey]["paths"]["assoluto"])
        if not os.path.exists(str(path_relativo_def)):
                print(f"Il file {path_relativo_def} non esiste. Passaggio saltato.")
                continue
        relative_path=Path(jsoncorrente[subkey]["paths"]["relativo"])
        parts = str(relative_path).split('/')
        # Prendi tutto tranne la prima parte
        relative_path_desinenza = '/'.join(parts[1:])
        relative_path_frequenza="/DataSetNasaInFrequenza"+relative_path_desinenza
        definitivo_path_frequenza=nuovo_path.joinpath(relative_path_desinenza)
        print(definitivo_path_frequenza)
        numero_di_sample=jsoncorrente[subkey]["shape"][0]
        print(numero_di_sample)
        dataset=ml.MatToDataFrame(path_relativo_def,key='singleData',IsColpitePath=True)
        datasetF=ml.analyze_audio_spectrum(dataset, number_of_samples=numero_di_sample, duration=60)
        data_dict = { 'singleData': datasetF.values }
        del dataset
        del datasetF
        #sio.savemat(path_relativo_def,data_dict)
            
            
            
print("ho finito")