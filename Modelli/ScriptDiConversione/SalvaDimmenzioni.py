import multiprocessing

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    
    import pandas as pd
    import MyLibrary as ml
    from pathlib import Path
    from tqdm import tqdm
    import dask.dataframe as dd
    import os
    import time
    from dask.distributed import Client, LocalCluster
    import re
    
    
    def estrai_numeri(chiave):
        # Trova tutti i numeri nella chiave
        numeri = re.findall(r'\d+', chiave)
        # Converte i numeri trovati in interi
        numeri = [int(numero) for numero in numeri]
        # Se ci sono numeri, restituisce i primi due (o aggiunge un infinito per garantire una coppia)
        return numeri

    def chiave_ordinamento(chiave):
        numeri = estrai_numeri(chiave)
        # Se ci sono numeri, usa il primo numero per il primo confronto, e la somma degli altri numeri per il secondo
        if len(numeri) > 0:
            primo_numero = numeri[0]
            somma_successivi = sum(numeri[1:])  # Somma dei numeri successivi al primo
        else:
            primo_numero = float('inf')
            somma_successivi = float('inf')
        return (primo_numero, somma_successivi)

    def ordina_dict_per_numeri(dizionario):
        # Ottiene le chiavi ordinate basate sulla chiave di ordinamento personalizzata
        chiavi_ordinate = sorted(dizionario.keys(), key=chiave_ordinamento)
        # Costruisce un nuovo dizionario usando l'ordine delle chiavi
        dizionario_ordinato = {chiave: dizionario[chiave] for chiave in chiavi_ordinate}
        return dizionario_ordinato

    # Configura Dask per utilizzare il LocalCluster
    cluster = LocalCluster(n_workers=os.cpu_count())
    client = Client(cluster)
    paths={}
    gestorePath=Path("json/NasaDataSetPath.json")
    json=Path("json/NasaDataSet")
    data = ml.read_json_file(r'json/NasaDataSet.json')
    nuovo_path = Path("/media/ailab/RAID0/giovannioliverio/DataSet2")
    print(nuovo_path)

    for key in data.keys():
        numero=key.split("_")[0]
        nj=numero+".json"
        salvajson=json.joinpath(nj)
        print(salvajson)
        dati=ml.read_json_file(salvajson) if salvajson.exists() else {}
        for subkey in tqdm(data[key].keys(), desc="Progresso"):
            if subkey != 'Header':
                path_relativo_def = nuovo_path.joinpath(data[key][subkey])
                print(path_relativo_def)
                inizio = time.time()
                print("Inizio lettura")
                
                dataset = ml.MatToDataFrame(path_relativo_def, key='singleData', IsColpitePath=True)
                t=f"{time.time() - inizio:.2f} secondi"
                print(f"Fine lettura in {t}")
                print(dataset.shape)
                shape = (dataset.shape[0], dataset.shape[1])
                del dataset
                
                new_data = {"shape": shape, "paths":{ "assoluto":str(path_relativo_def), "relativo": data[key][subkey]},"tempoApertura":t}
                print(new_data)
                
                dati[subkey] = new_data
        dati=ordina_dict_per_numeri(dati)
        ml.write_json_file(salvajson, dati)
        paths[numero]=str(salvajson)
    ml.write_json_file(gestorePath, paths)
