import re
import pandas as pd
import numpy as np
import unicodedata
import codecs

# traitement des plusieurs formes de dates dans une même colonne de DataFrame
date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d %B %Y']

def convert_dates(date_series, formats = date_formats):
    converted = pd.to_datetime(date_series, errors='coerce')
    for date_format in formats:
        converted = pd.to_datetime(date_series.where(converted.isna(), other=converted), format=date_format, errors='coerce')
    return converted

def remove_hex_escapes(text):
    if isinstance(text, str):
        return re.sub(r'\\x[0-9a-fA-F]{2}', '', text)
    return text

def decode_escaped_bytes(text):
    if not isinstance(text, str):
        return text
    try:
        return codecs.decode(text, 'unicode_escape').encode('latin1').decode('utf-8')
    except Exception:
        return text

def fill_missing_values(df, variable_principale): 

    maks_duplicated = df.duplicated(subset=[variable_principale])
    list_title = df.loc[maks_duplicated, variable_principale].to_list()

    list_columns = df.columns.tolist()
    list_columns.remove(variable_principale)

    for title in list_title:
        mask = df[variable_principale] == title

        for col in list_columns : 
            list_col = df.loc[mask,col].to_list()
            first_col = next(filter(pd.notna, list_col), None) # le premier élément non nul de la colonne
            df.loc[mask, col] = first_col

    # suppresion des duplications
    df = df.drop_duplicates(subset=[variable_principale], keep='first')
    
    return df

def complete_number_id(df) :
    try :
        mask = df['id'].astype(str).str.fullmatch(r'\s*') | df['id'].isna()
        list_id = df.loc[~mask, 'id'].astype(int).to_numpy()
        list_id_empty = np.random.randint(low = list_id.max()+1 , high = list_id.max() + len(mask.to_list())-len(list_id) +1 , dtype = int)

        df.loc[mask,'id'] = list_id_empty

        return df
    except : 
        return df
    
def normalize_text(text):
    if not isinstance(text, str):
        return ""

    # Ajouter un espace autour de chaque caractère non-alphanumérique sauf espace
    text = re.sub(r'([^\w\s])', r' \1 ', text)

    # Réduire les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()

    # Mise en minuscules
    text = text.lower()

    # Supprimer les accents
    text = unicodedata.normalize('NFKD', text).encode('ascii', errors='ignore').decode('utf-8')

    return text