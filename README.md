# **1. Guide d'installation de l'Environnement**

La première étape serait d'installer les librairies python, nécessaire au bon fonctionnement de la pipeline. 

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
```machine_learning_py3.12```. 

Pour désactiver l'environnement, il faut utiliser la commande suivante : 
```conda deactivate machine_learning_py3.12```. 

#### 1E. Vérifier l'installation :
Pour vérifier que l'environnement est activé et que les paquets sont installés, utilisez la commande suivante : ```conda list```. Cette commande listera tous les paquets installés dans l'environnement actif.

# **2. Arborescence de notre dossier**

```
techincal_test_servier/
│
├── __others__/        # Dossier sauvegardant les documents de présentation, etc.
│
├── raw_data/              # Données sources (CSV/JSON)
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   └── clinical_trials.csv
│
├── output_data/           # Dossier de sortie du fichier JSON final
│   └── drug_output.json
│
├── src/                   # Code source modulaire
│   ├── __init__.py
│   ├── loader.py          # Fonctions de chargement des fichiers
│   ├── processor.py       # Matching entre médicaments et publications
│   ├── graph_builder.py   # Construction du graphe final et sauvegarde
│   └── utils.py           # Fonctions utilitaires (nettoyage, encodage, etc.)
│
├── dags/                    # Dossier spécial pour Airflow
│   ├── __init__.py
│   └── dag_drug_pipeline.py  # Le DAG Airflow
│
├── main.py                # Script principal orchestrant toutes les étapes
│
├── journal_insight.py     # Traitement ad-hoc
│
├── environment.yml       # Dépendances du projet
│
└── README.md              # Documentation du projet
```

Dans ce dossier vous trouverez l'entièreté des éléments utiles pour le bon foctionnement de la pipeline. 

Pour pourvoir lancer la pipeline, il faut exécuter les étapes de la partie **1. Guide d'intallation de l'Environnement** et ensuite exécuter le fichier _main.py_. Vous retrouverez le json final sous le répertoire _output_data/drug_output.json_.

En sortie du pipeline, nous obtenons un JSON enregistrant une liste de dictionnaire respectant la structure du schéma comme ci-dessous (un dictionnaire fait référence à un médicament) :  

```
[
  {
    "drug_name": "diphenhydramine",
    "drug_id": "A04AD",
    "pubmed": [
      {
        "id": 1,
        "title": "a 44 - year - old man with erythema of the face diphenhydramine , neck , and chest , weakness , and palpitations",
        "date_mention": "2019-01-01"
      },
      {
        "id": 2,
        "title": "an evaluation of benadryl , pyribenzamine , and other so - called diphenhydramine antihistaminic drugs in the treatment of allergy .",
        "date_mention": "2019-01-01"
      },
      {
        "id": 3,
        "title": "diphenhydramine hydrochloride helps symptoms of ciguatera fish poisoning .",
        "date_mention": "2019-02-01"
      }
    ],
    "clinical_trials": [
      {
        "id": "NCT01967433",
        "title": "use of diphenhydramine as an adjunctive sedative for colonoscopy in patients chronically on opioids",
        "date_mention": "2020-01-01"
      },
      {
        "id": "NCT04189588",
        "title": "phase 2 study iv quzyttir TM ( cetirizine hydrochloride injection ) vs v diphenhydramine",
        "date_mention": "2020-01-01"
      },
      {
        "id": "NCT04237091",
        "title": "feasibility of a randomized controlled clinical trial comparing the use of cetirizine to replace diphenhydramine in the prevention of reactions related to paclitaxel",
        "date_mention": "2020-01-01"
      }
    ],
    "journal": {
      "journal of emergency nursing": [
        "2019-01-01",
        "2020-01-01"
      ],
      "the journal of pediatrics": [
        "2019-02-01"
      ]
    }
  }
    ]
```

Un autre structure sera proposé lors de la présentation, mais qui est tout à fait pertinent pour le cadre du projet.

Suite à la sortie du fichier JSON, nous pouvons le tester à traver un traitement ad-hoc via le fichier _journal_insight.py_. Le but serait de savoir quelle journal mentionne le plus de médicaments différents. La fonction dédiée à ce traitement est robuste à la forme du JSON en entrée, il peut détecter automatiquement la présence de la clé *journal*. 

Le résultat obtenu pour nos données est : 
```
Le journal mentionnant le plus de médicaments est :  JOURNAL OF EMERGENCY NURSING .

Il y a  2  médicaments mentionnées, qui sont :  {'epinephrine', 'diphenhydramine'} .
```

Dans le répertoire _dags/_ une première structuration du DAG est proposée et sera expliciter sera durant la présentation.

# **3. Pour aller plus loin ...**

>Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses
volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?
>
>Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de
telles volumétries ?

Dans le cadre d’une généralisation de la pipeline à des données de très grande volumétrie, il est essentiel de repenser le format des fichiers d’entrée. Pour des volumes de plusieurs téraoctets, les formats **CSV** ou **JSON** deviennent rapidement inefficaces, car ils impliquent une lecture **ligne par ligne**, donc de l’ensemble des données. À l’inverse, le format **Parquet**, basé sur une organisation **colonnaire**, permet une lecture plus rapide et sélective des données, ce qui en fait un choix bien plus adapté à un contexte Big Data.

> Site explicative - [Parquet](https://parquet.apache.org/docs/file-format/metadata/)

Par ailleurs, la librairie ``pandas``, bien qu’omniprésente pour le traitement de données, charge l'intégralité des fichiers en mémoire vive (RAM), ce qui la rend inadaptée dès que les volumes deviennent trop importants. Pour une montée en échelle tout en minimisant les modifications du code existant, il est pertinent d’utiliser la librairie ``dask``. Celle-ci permet une exécution **parallèle** des traitements en divisant les données en **blocs**, tout en conservant une API très proche de celle de ``pandas``. De plus, ``dask`` est **nativement compatible avec le format Parquet**, ce qui renforce la cohérence de cette solution.

> [Description de la librairie ``dask``](https://docs.dask.org/en/stable/dataframe.html) et sur [le traitement des fichiers parquet](https://docs.dask.org/en/latest/dataframe-parquet.html).

Concernant l’architecture de la pipeline, la structure actuelle, définie dans ``main.py``, suit une **logique linéaire et directive**, ce qui la rend **orchestrable**, mais **non orchestrée**. Dans une perspective Big Data, il serait plus approprié d’opter pour **une orchestration sous forme de DAG (Directed Acyclic Graph) à l’aide d’un outil comme Apache Airflow**.

> Site explicative - [DAG](https://www.datacamp.com/fr/blog/what-is-a-dag)

Actuellement, notre pipeline présente certaines limitations :
- La fonction `main()` enchaîne les étapes de manière linéaire, sans gestion explicite des dépendances entre les tâches, ce qui limite la flexibilité ;

- Les tâches ne sont pas conçues pour être exécutées de manière indépendante ou relancées isolément ;

- En cas d’échec d’une étape, l’ensemble du pipeline doit être relancé, faute de mécanismes de reprise ou de gestion d’erreurs à la tâche.
