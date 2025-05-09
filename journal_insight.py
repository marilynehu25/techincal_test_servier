import json
from collections import defaultdict

path = 'output_data\\'

with open(path + 'drug_output.json', 'r', encoding='utf-8') as fichier:
    data = json.load(fichier)

def ad_hoc_journal(data):

    journal_drug_map = defaultdict(set)

    for drug_entry in data:
        drug = drug_entry['drug_name']
        for source in ['pubmed', 'clinical_trials']:
            for mention in drug_entry.get(source, []):
                journal = mention['journal']
                journal_drug_map[journal].add(drug)

    # Chercher le journal avec le plus de drugs différents
    best_journal, drugs = max(journal_drug_map.items(), key=lambda x: len(x[1]))
    
    return best_journal, drugs

def main() : 
    best_journal, drugs = ad_hoc_journal(data)
    
    print('Le journal mentionnant le plus de médicaments est : ', best_journal.upper(), '.\n')
    
    print('Il y a ',len(drugs), ' médicaments mentionnées, qui sont : ', drugs, '.')

if __name__ == "__main__":
    main()
