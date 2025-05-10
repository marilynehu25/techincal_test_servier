import json
from collections import defaultdict

path = 'output_data\\'

with open(path + 'drug_output.json', 'r', encoding='utf-8') as fichier:
    data = json.load(fichier)

def ad_hoc_journal(data):
    journal_drug_map = defaultdict(set)

    for drug_entry in data:
        drug = drug_entry['drug_name']
        found_journal = False  # Indique si un journal a été trouvé via pubmed/clinical_trials

        # Cas 1 : journal dans pubmed/clinical_trials
        for source in ['pubmed', 'clinical_trials']:
            for mention in drug_entry.get(source, []):
                journal = mention.get('journal')
                if journal:
                    journal_drug_map[journal].add(drug)
                    found_journal = True

        # Cas 2 : journal dans 'journal' (utilisé uniquement si aucun trouvé avant)
        if not found_journal:
            for journal in drug_entry.get('journal', {}):
                journal_drug_map[journal].add(drug)

    best_journal, drugs = max(journal_drug_map.items(), key=lambda x: len(x[1]), default=(None, set()))

    return best_journal, drugs

def main() : 
    best_journal, drugs = ad_hoc_journal(data)
    
    if best_journal == None : 
        print('Les journaux ne sont pas référencés.')

    else : 
        print('Le journal mentionnant le plus de médicaments est : ', best_journal.upper(), '.\n')
        print('Il y a ',len(drugs), ' médicaments mentionnées, qui sont : ', drugs, '.')

if __name__ == "__main__":
    main()
