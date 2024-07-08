import os

def find_project_root(start_dir, rootName="VegaTesi"):
    """
    Trova la cartella radice del progetto risalendo nella struttura delle cartelle.

    Args:
        start_dir (str): La directory di partenza per la ricerca.
        rootName (str, optional): Il nome della cartella radice del progetto. Default: "VegaTesi".

    Returns:
        str: Il percorso assoluto della cartella radice del progetto.
    """
    current_dir = os.path.abspath(start_dir)
    while True:
        # Controlla se il nome della cartella corrente è "VegaTesi"
        if os.path.basename(current_dir) == rootName:
            return current_dir
        # Vai alla cartella genitore
        parent_dir = os.path.dirname(current_dir)
        # Se sei già nella radice, interrompi la ricerca
        if current_dir == parent_dir:
            raise FileNotFoundError("Cartella VegaTesi non trovata nel percorso del progetto.")
        current_dir = parent_dir
        
def find_project_root_fromPath(path, rootName="VegaTesi"):
    """_summary_

    Args:
        path (_type_): _description_
        rootName (str, optional): _description_. Defaults to "VegaTesi".

    Returns:
        _type_: _description_
    """
    return find_project_root(os.path.dirname(path), rootName)

def generatore_path(path, estensione):
    """_summary_

    Args:
        path (_type_): _description_
        estensione (_type_): _description_

    Returns:
        _type_: _description_
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(estensione):
                yield os.path.join(root, file)

def path_from_root(path, resto_del_path, nome_root="tesi"):
    """
        Genera il percorso assoluto di un file patendo dal percorso relativo rispetto al progetto
        trova la root del progetto e concatena il resto del percorso.
    Args:
        path (_type_): path di partenza per la ricerca della root del progetto
        resto_del_path (_type_): percorso relativo rispetto alla root del progetto
        rootName (str, optional): Il nome della cartella radice del progetto. Default: "VegaTesi".

    Returns:
        str: il percorso assoluto del file
    """
    root = find_project_root_fromPath(path, nome_root)
    return os.path.join(root, resto_del_path)