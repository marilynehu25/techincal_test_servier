import pandas as pd
import json

def read_csv(path, encoding='utf-8', index_col = None):
    try:
        # Première tentative avec virgule comme séparateur
        return pd.read_csv(path, sep=',', encoding=encoding, index_col=index_col)
    except Exception as e1:
        try:
            # Deuxième tentative avec point-virgule
            return pd.read_csv(path, sep=';', encoding=encoding, index_col = index_col)
        except Exception as e2:
            print("Erreur avec ',':", e1)
            print("Erreur avec ';':", e2)
            return None

def read_json(path, encoding = 'utf-8') : 
    with open(path, 'r', encoding='utf-8') as fichier:
        data = json.load(fichier)
    
    df = pd.DataFrame(data)

    return df