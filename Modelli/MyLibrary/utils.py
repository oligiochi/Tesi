import numpy as np
from sklearn.metrics import *
from scipy.stats import pearsonr, spearmanr
from sklearn.base import BaseEstimator, TransformerMixin

def splitInputOutput(data, outputColumns):
    """
    Divide il DataFrame in input e output in base alle colonne specificate come output.
    
    Parameters:
        data (DataFrame): Il DataFrame da dividere
        outputColumns (list): Una lista delle colonne da considerare come output
        
    Returns:
        DataFrame, DataFrame: Il DataFrame contenente le colonne di input e il DataFrame contenente le colonne di output
    """
    # Trova le colonne di input escludendo quelle specificate come output
    inputColumns = [col for col in data.columns if col not in outputColumns]
    
    # Restituisce il DataFrame con le colonne di input e il DataFrame con le colonne di output
    return data[inputColumns], data[outputColumns]

def allStatistic(y_train,y_train_pred,y_test, y_test_pred):
    """
    Calcola una serie di statistiche di valutazione del modello su set di dati di addestramento e test.

    Questa funzione calcola diverse metriche di valutazione del modello, tra cui l'errore assoluto medio (MAE),
    l'errore quadratico medio (MSE), la radice dell'errore quadratico medio (RMSE), l'errore percentuale assoluto medio (MAPE),
    il coefficiente di determinazione (R²), il coefficiente di correlazione di Pearson e il coefficiente di correlazione di Spearman.

    Parameters:
        y_train (array-like): Valori target effettivi per il set di addestramento.
        y_train_pred (array-like): Valori predetti dal modello per il set di addestramento.
        y_test (array-like): Valori target effettivi per il set di test.
        y_test_pred (array-like): Valori predetti dal modello per il set di test.

    Returns:
        dict: Un dizionario contenente le statistiche calcolate per il set di addestramento e di test.
    """
    mae_train = mean_absolute_error(y_train, y_train_pred)
    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = np.sqrt(mse_train)
    mape_train = mean_absolute_percentage_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)
    #pearson_train = pearsonr(y_train, y_train_pred)[0]
    spearman_train = spearmanr(y_train, y_train_pred)[0]
    mae_test = mean_absolute_error(y_test, y_test_pred)
    mse_test = mean_squared_error(y_test, y_test_pred)
    rmse_test = np.sqrt(mse_test)
    mape_test = mean_absolute_percentage_error(y_test, y_test_pred)
    r2_test = r2_score(y_test, y_test_pred)
    #pearson_test = pearsonr(y_test, y_test_pred)[0]
    spearman_test = spearmanr(y_test, y_test_pred)[0]
    statistics = {
        "MAE_train": mae_train,
        "MSE_train": mse_train,
        "RMSE_train": rmse_train,
        "MAPE_train": mape_train,
        "R2_train": r2_train,
        #"Pearson_train": pearson_train,
        "Spearman_train": spearman_train,
        "MAE_test": mae_test,
        "MSE_test": mse_test,
        "RMSE_test": rmse_test,
        "MAPE_test": mape_test,
        "R2_test": r2_test,
        #"Pearson_test": pearson_test,
        "Spearman_test": spearman_test
    }
    return statistics

class NoneScaler(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X
    
    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)