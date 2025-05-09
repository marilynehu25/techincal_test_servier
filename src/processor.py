import re
from joblib import Parallel, delayed
from tqdm import tqdm

# recherche des noms de médicaments dans une colonne d'un dataframe
def find_drugs(df, drug_name, columns_name) : 
    # forme du mot à rechercher
    pattern = rf'\b{re.escape(drug_name)}\b'
    # filtre sur la colonne contenant les noms de médicaments
    mask = df[columns_name].str.contains(pattern, case=False, na = False)
    # extraction des index des lignes contenant le médicament
    list_index = df[mask].index.tolist()

    return (drug_name,list_index)

def get_index_drug(df,list_drugs,title_columns) : 
    
    index = dict(Parallel(n_jobs=-1)(delayed(find_drugs)(df, drugs_name, title_columns)
    for drugs_name in tqdm(list_drugs)))

    return index



