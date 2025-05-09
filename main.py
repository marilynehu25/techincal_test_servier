import pandas as pd
from src.loader import read_csv , read_json
from src.utils import normalize_text , remove_hex_escapes , convert_dates, fill_missing_values, complete_number_id, decode_escaped_bytes
from src.processor import get_index_drug
from src.graph_builder import final_json, save_to_json

def load_data(path) : 
    
    #chargement des données bruts
    df_clinicals_trials = read_csv(path + 'clinical_trials.csv')
    df_drugs = read_csv(path + 'drugs.csv')
    df_pubmed1 = read_csv(path + 'pubmed.csv')
    df_pubmed2 = read_json(path + 'pubmed.json')
    
    return df_clinicals_trials , df_drugs, df_pubmed1, df_pubmed2
    

# 1.traitement des publications sur les test cliniques

def clean_clinicals_trials(df) :
    df_clinicals_trials = df
    
    # compléter les colonnes vides avec un même titre scientifique
    df_clinicals_trials = fill_missing_values(df_clinicals_trials, 'scientific_title')
    
    # suppession des lignes sans scientific_title
    mask_space = df_clinicals_trials['scientific_title'].str.strip() == ''
    df_clinicals_trials = df_clinicals_trials[~mask_space].dropna(subset=['scientific_title'])
    
    # convertion de la colonne date
    df_clinicals_trials['date'] = convert_dates(df_clinicals_trials['date'])
    
    # décodage des mots mal codés
    df_clinicals_trials['scientific_title'] = df_clinicals_trials['scientific_title'].apply(decode_escaped_bytes)
    
    # décodage des colonnes avec erreurs
    df_clinicals_trials.loc[:,'journal'] = df_clinicals_trials['journal'].apply(remove_hex_escapes)
    df_clinicals_trials.loc[:,'scientific_title'] = df_clinicals_trials['scientific_title'].apply(remove_hex_escapes)
    
    # formater les titres scientifiques en minuscules
    df_clinicals_trials.loc[:,'scientific_title'] = df_clinicals_trials['scientific_title'].apply(normalize_text)
    df_clinicals_trials.loc[:,'journal'] = df_clinicals_trials['journal'].apply(normalize_text)
    
    # mettre la colonne des id en index
    df_clinicals_trials = df_clinicals_trials.set_index(df_clinicals_trials.columns[0])
    
    return df_clinicals_trials

# 2. Traitement des données médicaments

def clean_drugs(df) : 
    df_drugs = df
    # traitement des noms de médicaments
    df_drugs['drug'] = df_drugs['drug'].apply(normalize_text)
    
    return df_drugs
    
# 3. Traitement des publications de types pubmed

def clean_pubmed(df1, df2) : 
    df_pubmed1 = df1
    df_pubmed2 = df2
    
    # compléter l'id qui manque
    df_pubmed1 = complete_number_id(df_pubmed1)
    df_pubmed2 = complete_number_id(df_pubmed2)
    
    # concaténation des dataframes
    df_pubmed = pd.concat([df_pubmed1, df_pubmed2], axis=0, ignore_index=True)
    
    # uniformisation des dates de publications
    df_pubmed['date'] = convert_dates(df_pubmed['date'])
    
    # normalisation des titres de publications et de journaux
    df_pubmed['title'] = df_pubmed['title'].apply(normalize_text)
    df_pubmed['journal'] = df_pubmed['journal'].apply(normalize_text)
    
    # mettre l'id en index 
    df_pubmed = df_pubmed.set_index(df_pubmed.columns[0])
    
    return df_pubmed

# 3. Liaison des médicaments

def get_links(df_clinicals_trials , df_drugs, df_pubmed) : 
    
    # établissmeent de la liste de drugs
    list_drugs = df_drugs['drug'].tolist()
    
    # établissement de la liste d'id des drugs 
    list_drugs_id = df_drugs['atccode'].tolist()
    
    # création du dictionnaire où pour chaque drug on associe sa liste d'index du dataframe
    index_clinicals_trials = get_index_drug(df = df_clinicals_trials, title_columns= 'scientific_title', list_drugs= list_drugs)
    index_pubmed = get_index_drug(df = df_pubmed, title_columns= 'title', list_drugs= list_drugs)
    
    return list_drugs, list_drugs_id, index_clinicals_trials, index_pubmed

# 4. Obtention du json final

def build_json(dictionnaire_df, list_drugs, list_drugs_id = None) : 

    output_final = final_json(dictionnaire_df,list_drugs,list_drugs_id)
    
    # sauvegarde du fichier de sortie
    path_output = r'output_data/'
    
    save_to_json(output_final, path_output + 'drug_output.json')
    
    print('\n\nBINGO ! La pipeline fonctionne !')


def main() : 
    path = r'raw_data/'
    df_clinicals_trials , df_drugs, df_pubmed1, df_pubmed2 = load_data(path)
    
    df_clinicals_trials = clean_clinicals_trials(df_clinicals_trials)
    
    df_drugs = clean_drugs(df_drugs)
    
    df_pubmed = clean_pubmed(df_pubmed1, df_pubmed2)
    
    list_drugs, list_drugs_id, index_clinicals_trials, index_pubmed = get_links(df_clinicals_trials , df_drugs, df_pubmed)
    
    dictionnaire_df = [{'nom_mention' : 'pubmed' , 'df' : df_pubmed, 'index' : index_pubmed, 'title' : 'title', 'date_mention':'date',
                    'journal' : 'journal'} , 
                    {'nom_mention' : 'clinical_trials' , 'df' : df_clinicals_trials, 'index' : index_clinicals_trials, 'title' : 'scientific_title', 
                    'date_mention':'date', 'journal' : 'journal'}]
    
    build_json(dictionnaire_df, list_drugs, list_drugs_id)
    
if __name__ == "__main__":
    main()