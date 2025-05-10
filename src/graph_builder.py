import pandas as pd
from tqdm import tqdm
import json
import os
import numpy as np

journal_json = True 
link_journal_pub = False

def final_json(dictionnaire_df, list_drugs, list_drugs_id = False, journal_json = journal_json, link_journal_pub = link_journal_pub) : 

    """
    VARIABLES : 
        - dictionnaire_df : le dictionnaire qui rassemble les dataframes à gérer avec les noms de colonnes associés à chaque élément
        correspondant. 
            Par exemple pour le cas de notre test : 
                dictionnaire_df = [{'nom_mention' : 'pubmed' , 'df' : df_pubmed, 'index' : index_pubmed, 'title' : 'title', 'date_mention':'date',
                'journal' : 'journal'} , 
                {'nom_mention' : 'clinical_trials' , 'df' : df_clinicals_trials, 'index' : index_clinical_trials, 'title' : 'scientific_title', 
                'date_mention':'date', 'journal' : 'journal'}]
            Les clés suivant : 
                - 'nom_mention' : le nom de la catégorie de mention 
                - 'df' : le dataframe associé à la catégorie de mention
                - 'index' : le dictionnaire où chaque drug est associé à la liste des index où le drug est mentionné dans le titre de la publication
                - 'title' : le nom de la colonne du titre des publications dans le dataframe
                - 'date_mention' : le nom de la colonne de la date des publications dans le dataframe
                - 'journal' : le nom de la colonne des journaux dans le dataframe
        - list_drugs : la liste des noms de drug
        - list_drugs_id : la liste des id de drug (optionnel)
        - journal_json = False : variable booléen indiquant si on ajoute la clé 'journal' comme lien direct
        - link_journal_pub = True : variable booléen indiquant si on fait apparaître la relation entre les publications et le journal
    
    DESCRIPTION : 
        Cette fonction a pour but de générer une liste de dictionnaire pour chaque drug où on associe les publications et journaux
        mentionnant son nom, ainsi que sa date de mention dans chaque publication.
        On a volairement choisi par défaut la liaison indirecte des journaux car ça donne une structure plus précise : (journal_json = False, link_journal_pub = True).
        Si on veut la structure directe des publications et des journaux, on doit avoir : (journal_json = True, link_journal_pub = False).
        Si on souhaite avoir les deux, on peut saisir : (journal_json = True, link_journal_pub = True).

    SORTIE :
        En sortie, on a une liste de la forme suivante pour 1 drug si on a (journal_json = True, link_journal_pub = True) : 
            [
                {
                    'drug_name': 'epinephrine',
                    'drug_id': 'A01AD',
                    'pubmed': [{'id': 7,
                    'title': 'the high cost of epinephrine autoinjectors and possible alternatives.',
                    'date_mention': '2020-01-02',
                    'journal': 'the journal of allergy and clinical immunology. in practice'},
                    {'id': 8,
                    'title': 'time to epinephrine treatment is associated with the risk of mortality in children who achieve sustained rosc after traumatic out-of-hospital cardiac arrest.',
                    'date_mention': '2020-01-03',
                    'journal': 'the journal of allergy and clinical immunology. in practice'}],
                    'clinical_trials': [{'id': 'NCT04188184',
                    'title': 'tranexamic acid versus epinephrine during exploratory tympanotomy',
                    'date_mention': '2020-04-27',
                    'journal': 'journal of emergency nursing'}] ,
                    'journal' : {'journal of emergency nursing' : ["2019-01-01", "2020-04-27"]}
                        }
                            ]
    """

    # liste de sortie avec un dictionnaire par drug
    final_json = []

    # itération sur les drugs
    for n, drugs in tqdm(enumerate(list_drugs)): 

        # le dictionnaire associé au drug
        diction_json = {}

        # le nom du drug
        diction_json['drug_name'] = drugs

        # l'id du drug
        if list_drugs_id : 
            diction_json['drug_id'] = list_drugs_id[n]

        # itération sur tous les dataframes de publications
        for diction in tqdm(dictionnaire_df): 

            # dataframe de publication
            df = diction['df']

            # liste de dictionnaire de la mention qui sauvegarde toutes les publications mentionnant le drug 
            diction_json[diction['nom_mention']] = []

            # itération sur la liste d'index du médicament
            for idx in diction['index'][drugs] : 
                # récupération des lignes de publication dans le dataframe où le drug est mentionné
                data = df.loc[idx]

                # écriture du dictionnaire associé à la publication
                if link_journal_pub : 
                    dict_idx = {'id' : idx , 
                        'title' : data[diction['title']] , 
                        'date_mention' : data[diction['date_mention']], 
                        'journal' : data[diction['journal']]}
                else : 
                    dict_idx = {'id' : idx , 
                        'title' : data[diction['title']] , 
                        'date_mention' : data[diction['date_mention']]}
                
                # ajout du dictionnaire de la publication dans la liste de la mention associé
                diction_json[diction['nom_mention']].append(dict_idx)
        
        # choix d'ajout de la clé 'journal
        if journal_json : 

            # création de la clé 'journal'
            diction_json['journal'] = {}

            # itération sur tous les dataframes de publications
            for diction in tqdm(dictionnaire_df): 

                # dataframe de publication
                df = diction['df']
                # extraction de toutes la plage de datafrme pour le drug
                data_drug_journal = df.loc[diction['index'][drugs]]
                # obtention de la liste des journaux du dataframe
                list_journal = data_drug_journal['journal'].unique().tolist()
                # itération sur les journaux un par un
                for journal in list_journal : 
                    # extraction de la liste de date pour le journal associé
                    mask_journal_date = data_drug_journal['journal'] == journal
                    list_data_journal = data_drug_journal.loc[mask_journal_date,'date'].tolist()

                    # ajout de nouvelles éléments si le journal existe déjà
                    if journal in diction_json['journal'].keys() : 
                        diction_json['journal'][journal] = diction_json['journal'][journal] + list_data_journal
                    # affectation de nouvelle élément si le journal n'existe pas encore dans le dictionnaire
                    else : 
                        diction_json['journal'][journal] = list_data_journal
                    # enlève les duplications dans les listes de dates
                    diction_json['journal'][journal] = list(set(diction_json['journal'][journal]))
            
        # ajout du dictionnaire associé au drug à la liste de sortie
        final_json.append(diction_json)
        
    return final_json

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        elif isinstance(obj, (np.floating, float)):
            return float(obj)
        elif isinstance(obj, (np.ndarray, list)):
            return list(obj)
        elif isinstance(obj, (pd.Timestamp,)):
            return obj.strftime('%Y-%m-%d') 
        return super().default(obj)

def save_to_json(data, filepath, indent=2, ensure_ascii=False):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, cls=EnhancedJSONEncoder)
