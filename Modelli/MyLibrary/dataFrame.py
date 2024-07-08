import array
import re
import scipy.io as sio
import pandas as pd
from . import file_utils as fu

def loadDataSetFromMat(pathDataSet, IsColpitePath=False):
    """
    Carica un file .mat e restituisce i dati contenuti.
    
    Parameters:
        pathDataSet (str): Il percorso del file .mat
        
    Returns:
        dict: I dati contenuti nel file .mat
    """
    if IsColpitePath:
        pathDataSet=fu.path_from_root(__file__,pathDataSet)
    return sio.loadmat(pathDataSet)

def MatToDataFrame(pathDataSet, key='DATI_AVIO_VEGA', IsColpitePath=False):
    """
    Carica i dati da un file .mat e li converte in un DataFrame Pandas.
    
    Parameters:
        pathDataSet (str): Il percorso del file .mat
        
    Returns:
        DataFrame: Il DataFrame contenente i dati
    """
    return pd.DataFrame(loadDataSetFromMat(pathDataSet,IsColpitePath)[key])

def RenameColumns(pathDataSet):
    """
    Carica i dati da un file .mat, li converte in un DataFrame Pandas e rinomina le colonne.
    
    Parameters:
        pathDataSet (str): Il percorso del file .mat
        
    Returns:
        DataFrame: Il DataFrame contenente i dati con le colonne rinominate
    """
    ds=MatToDataFrame(pathDataSet)
    ds.rename(columns={0:'Velocità',1:'Angolo',2:'X Sensore',3:'Frequenza',4:'Pressione'}, inplace=True)
    ds['X Sensore'] = ds['X Sensore'].astype(int)
    return ds

def generaFiltro(ds, colonne, valori):
    """
    Genera un filtro basato sui valori delle colonne del DataFrame.
    
    Parameters:
        ds (DataFrame): Il DataFrame su cui applicare il filtro
        colonne (list): Una lista delle colonne da considerare nel filtro
        valori (list): Una lista di liste, ciascuna contenente i valori da verificare per la corrispondente colonna
        
    Returns:
        Series: La serie booleana risultante dopo l'applicazione del filtro
    """
    filtro=True
    for colonna, valori_colonna in zip(colonne, valori):
        filtro = filtro & ds[colonna].isin(valori_colonna)
    return filtro

def FilterDataFrameFiltrato(ds,filtro):
    """
    Filtra un DataFrame utilizzando una serie booleana.
    
    Parameters:
        ds (DataFrame): Il DataFrame da filtrare
        filtro (Series): La serie booleana da utilizzare come filtro
        
    Returns:
        DataFrame: Il DataFrame risultante dopo il filtraggio
    """
    return ds[filtro]

def FilterDataFrame(ds:pd.DataFrame,colonne:list,valori:list):
    """
    Applica un filtro a un DataFrame basato sui valori delle colonne.
    
    Parameters:
        ds (DataFrame): Il DataFrame su cui applicare il filtro
        colonne (list): Una lista delle colonne da considerare nel filtro
        valori (list): Una lista di liste, ciascuna contenente i valori da verificare per la corrispondente colonna
        
    Returns:
        DataFrame: Il DataFrame risultante dopo il filtraggio
    """
    filtro=generaFiltro(ds, colonne, valori)
    return FilterDataFrameFiltrato(ds, filtro)

def SensoriDataSet(sensoriDataSetPath:str):
    """
    Carica un file CSV contenente dati sui sensori e rimuove eventuali caratteri non stampabili.
    
    Parameters:
        sensoriDataSetPath (str): Il percorso del file CSV
        
    Returns:
        DataFrame: Il DataFrame contenente i dati sui sensori
    """
    sensoriDataSetPath=fu.path_from_root(__file__,sensoriDataSetPath)
    sensori=pd.read_csv(sensoriDataSetPath)
    sensori=sensori.replace('\u200b','',regex=True)
    return sensori

def CreaDictionary(df:pd.DataFrame, colonnaChiave:str, colonnaValore:str):
    """
    Crea un dizionario a partire da un DataFrame utilizzando due colonne come chiave e valore.
    
    Parameters:
        df (DataFrame): Il DataFrame da cui estrarre i dati per creare il dizionario
        colonnaChiave (str): Il nome della colonna da utilizzare come chiave del dizionario
        colonnaValore (str): Il nome della colonna da utilizzare come valore del dizionario
        
    Returns:
        dict: Il dizionario creato utilizzando i dati dal DataFrame
    """
    return dict(zip(df[colonnaChiave], df[colonnaValore]))

def MappaturaDataFrame(df:pd.DataFrame, colonnaNuova:str, colonnaDaMappare:str, dictionary:dict):
    """
    Crea una nuova colonna in un DataFrame mappando i valori di una colonna esistente utilizzando un dizionario.
    
    Parameters:
        df (DataFrame): Il DataFrame su cui applicare la mappatura
        colonnaNuova (str): Il nome della nuova colonna da creare
        colonnaDaMappare (str): Il nome della colonna esistente da cui estrarre i valori
        dictionary (dict): Il dizionario utilizzato per mappare i valori
        
    Returns:
        DataFrame: Il DataFrame con la nuova colonna creata
    """
    dout=df.copy()
    dout[colonnaNuova]=df[colonnaDaMappare].map(dictionary)
    return dout
