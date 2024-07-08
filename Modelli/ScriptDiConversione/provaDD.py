import pandas as pd
import MyLibrary as ml
from pathlib import Path
from tqdm import tqdm
import dask.dataframe as dd
import os

path="/media/ailab/RAID0/giovannioliverio/DataSetNasa/B101/B101/Channel1.csv"
path=Path(path)
blocksize = os.path.getsize(path)
data=dd.read_table(path, blocksize=blocksize,sample=blocksize)
print(data.head(len(data)))