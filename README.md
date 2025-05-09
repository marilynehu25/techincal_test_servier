# **1. Guide d'installation de l'Environnement**

Pour pouvoir effectuer les TD du cours de *Machine Learning*, il faut créer un environnement virtuel et installer les librairies nécessaires.

Ce guide vous explique comment configurer votre environnement de développement en utilisant un fichier `environment.yml` avec Conda.

>**Prérequis :** Assurez-vous que [Conda](https://docs.conda.io/en/latest/) est installé sur votre machine. Conda est inclus avec [Anaconda](https://www.anaconda.com/products/distribution) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Suivez les étapes suivantes pour intaller l'environnement : 

#### 1A. Ouvrir un terminal ou une invite de commande :

- Sur Windows, vous pouvez utiliser l'invite de commandes _Anaconda Prompt_.
- Sur macOS ou Linux, ouvrez un terminal.

#### 1B. Naviguer jusqu'au répertoire contenant le fichier ``environment.yml`` :

Utilisez la commande `cd` pour naviguer jusqu'au répertoire où se trouve votre fichier `environment.yml`. Par exemple : ```cd chemin/vers/votre/repertoire```.

#### 1C. Créer l'environnement à partir du fichier `environment.yml` :
Exécutez la commande suivante pour créer l'environnement : 
```conda env create -f environment.yml```.
Cette commande lira le fichier `environment.yml` et installera toutes les dépendances spécifiées dans un nouvel environnement Conda.

#### 1D. Activer/Désactiver l'environnement :
Une fois l'environnement créé, activez-le en utilisant la commande suivante : 
```conda activate machine_learning_py3.12```. 

Pour désactiver l'environnement, il faut utiliser la commande suivante : 
```conda deactivate machine_learning_py3.12```. 

#### 1E. Vérifier l'installation :
Pour vérifier que l'environnement est activé et que les paquets sont installés, utilisez la commande suivante : ```conda list```. Cette commande listera tous les paquets installés dans l'environnement actif.

# **2. Arborescence de notre dossier**

drug_graph_pipeline/
│
├── data/                      # (optionnel) Données en entrée si test local
│
├── raw_data/                  # Données sources (CSV/JSON)
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   └── clinical_trials.csv
│
├── output_data/               # Dossier de sortie du fichier JSON final
│   └── drug_output.json
│
├── src/                       # Code source modulaire
│   ├── __init__.py
│   ├── loader.py             # Fonctions de chargement des fichiers
│   ├── processor.py          # Matching entre médicaments et publications
│   ├── graph_builder.py      # Construction du graphe final et sauvegarde
│   └── utils.py              # Fonctions utilitaires (nettoyage, encodage, etc.)
│
├── main.py                   # Script principal orchestrant toutes les étapes
├── requirements.txt          # Dépendances du projet
└── README.md                 # Documentation du projet


