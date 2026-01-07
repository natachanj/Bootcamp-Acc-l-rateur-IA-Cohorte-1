# Analyse de Marché des Emplois Tech

> Un projet complet pour scraper, analyser et visualiser les tendances du marché de l'emploi dans le secteur technologique.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)

## Dépôt GitHub

Ce projet fait partie du dépôt [Bootcamp-Acc-l-rateur-IA-Cohorte-1](https://github.com/natachanj/Bootcamp-Acc-l-rateur-IA-Cohorte-1.git).

**Chemin dans le dépôt :** `Semaine 1/Session 1/ProjetAnalyseMarchéEmploi/`

Pour cloner le projet complet :
```bash
git clone https://github.com/natachanj/Bootcamp-Acc-l-rateur-IA-Cohorte-1.git
cd "Bootcamp-Acc-l-rateur-IA-Cohorte-1/Semaine 1/Session  1/ProjetAnalyseMarchéEmploi"
```

## Table des Matières

- [Dépôt GitHub](#dépôt-github)
- [Description du Projet](#description-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation Rapide](#utilisation-rapide)
- [Structure du Projet](#structure-du-projet)
- [Technologies Utilisées](#technologies-utilisées)
- [Guide Complet](#guide-complet)
- [Résolution de Problèmes](#résolution-de-problèmes)
- [Contributions](#contributions)
- [Ressources](#ressources)

## Description du Projet

Ce projet éducatif vous permet de :

1. **Scraper des données** depuis des sites d'emploi tech spécialisés
2. **Analyser les tendances** du marché de l'emploi technologique
3. **Visualiser les données** avec un dashboard interactif et moderne
4. **Identifier les opportunités** : types de contrats, technologies recherchées, salaires

### Objectifs Pédagogiques

- Maîtriser le **web scraping** avec BeautifulSoup et requests
- Traiter et nettoyer des données avec **pandas**
- Créer des visualisations interactives avec **Streamlit** et **Plotly**
- Analyser le marché de l'emploi tech pour comprendre les tendances
- Extraire automatiquement des informations structurées depuis du texte non structuré

## Fonctionnalités

### Partie 1 : Scraping des Données (`Partie1-scraper_emplois.ipynb`)

- **Scraping multi-sites** : Collecte d'offres depuis plusieurs pays/régions
- **Extraction intelligente** : Détection automatique de :
  - Types de contrats (Remote/Hybrid/On-site)
  - Niveaux d'expérience requis (Junior/Mid-level/Senior)
  - Stack technique recherchée (Python, React, AWS, etc.)
  - Fourchettes salariales
- **Nettoyage automatique** : Traitement et normalisation des données
- **Export CSV** : Sauvegarde structurée pour analyse ultérieure

### Partie 2 : Dashboard Interactif (`Partie2_tableau_bord_marche_emploi.py`)

- **Statistiques globales** : Vue d'ensemble du marché
- **Analyse géographique** : Répartition des opportunités par localisation
- **Types de contrats** : Analyse Remote vs Hybrid vs On-site
- **Niveaux d'expérience** : Distribution des postes par niveau requis
- **Technologies recherchées** : Top technologies et stack technique
- **Analyse salariale** : Salaires moyens par localisation et type de contrat
- **Filtres avancés** : Recherche et filtrage multi-critères
- **Export de données** : Téléchargement des données filtrées en CSV

## Prérequis

- **Python 3.8+** (recommandé : Python 3.10+)
- **pip** ou **uv** (gestionnaire de paquets)
- **Connexion Internet** (pour le scraping)
- **Navigateur web** (pour visualiser le dashboard)

## Installation

### Option 1 : Avec uv (Recommandé - Plus rapide)

```bash
# Cloner ou télécharger le projet
cd ProjetAnalyseMarchéEmploi

# Installer les dépendances avec uv
uv sync

# Lancer Jupyter Notebook
uv run jupyter notebook
```

### Option 2 : Avec Python standard

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer Jupyter Notebook
jupyter notebook
```

### Vérification de l'installation

```bash
# Vérifier que Python est installé
python --version

# Vérifier que les packages sont installés
python -c "import pandas, streamlit, plotly; print('Toutes les dépendances sont installées')"
```

## Utilisation Rapide

### Étape 1 : Scraper les données

1. **Ouvrir Jupyter Notebook** :
   ```bash
   uv run jupyter notebook
   # ou
   jupyter notebook
   ```

2. **Ouvrir le notebook** : `Partie1-scraper_emplois.ipynb`

3. **Exécuter les cellules** dans l'ordre (Shift + Enter)

4. **Vérifier les données** : Les données seront sauvegardées dans `data/donnees_marche_emploi.csv`

### Étape 2 : Visualiser avec le dashboard

```bash
# Lancer le dashboard Streamlit
streamlit run Partie2_tableau_bord_marche_emploi.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

> **Astuce** : Si vous n'avez pas encore de données scrapées, vous pouvez utiliser les données d'exemple :
> ```bash
> cp examples/donnees_emploi_echantillon.csv data/donnees_marche_emploi.csv
> ```

## Structure du Projet

```
ProjetAnalyseMarchéEmploi/
│
├── README.md                          # Ce fichier - Documentation principale
├── GUIDE_UTILISATION.md              # Guide détaillé d'utilisation
├── requirements.txt                   # Dépendances Python
├── pyproject.toml                     # Configuration du projet (uv)
│
├── Partie1-scraper_emplois.ipynb     # Notebook de scraping
├── Partie2_tableau_bord_marche_emploi.py  # Dashboard Streamlit
│
├── data/
│   └── donnees_marche_emploi.csv        # Données scrapées (généré)
│
└── examples/
    ├── donnees_echantillon.csv          # Données d'exemple génériques
    └── donnees_emploi_echantillon.csv   # Données d'exemple pour tester le dashboard
```

## Technologies Utilisées

| Technologie | Version | Usage |
|------------|---------|-------|
| **Python** | 3.8+ | Langage de programmation |
| **BeautifulSoup4** | 4.12+ | Parsing HTML et extraction de données |
| **Requests** | 2.31+ | Requêtes HTTP pour le scraping |
| **Pandas** | 2.0+ | Manipulation et analyse de données |
| **NumPy** | 1.24+ | Calculs numériques |
| **Streamlit** | 1.28+ | Interface web interactive |
| **Plotly** | 5.17+ | Visualisations interactives |
| **Jupyter Notebook** | 6.0+ | Environnement de développement |
| **lxml** | 4.9+ | Parser XML/HTML rapide |

## Guide Complet

Pour des instructions détaillées, consultez le **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** qui contient :

- Instructions pas à pas
- Notes pédagogiques pour les étudiants
- Exercices suggérés (Débutant, Intermédiaire, Avancé)
- Guide de résolution de problèmes
- Ressources complémentaires

## Ce qui Rend ce Projet Unique

Ce projet se distingue des autres projets similaires par :

1. **Focus marché du travail** : Analyse des tendances plutôt que des compétences individuelles
2. **Extraction intelligente** : Détection automatique depuis le texte non structuré
3. **Analyse multi-régionale** : Comparaison des opportunités entre pays
4. **Types de contrats** : Analyse détaillée Remote/Hybrid/On-site
5. **Stack technique** : Identification automatique des technologies recherchées
6. **Visualisations avancées** : Dashboard interactif avec filtres multiples

## Notes Importantes

### Éthique et Légalité

- **Respectez les conditions d'utilisation** des sites web
- **Vérifiez robots.txt** avant de scraper
- **Utilisez des délais** entre les requêtes (minimum 2 secondes)
- **Ne surchargez pas** les serveurs
- **Ce projet est à des fins éducatives uniquement**

### Bonnes Pratiques

- Testez d'abord sur une seule page avant de scraper en masse
- Inspectez le code HTML avec les outils développeur
- Gérez les erreurs avec des try/except
- Sauvegardez régulièrement vos données

## Résolution de Problèmes

### Le scraping ne fonctionne pas

- Vérifiez votre connexion Internet
- Vérifiez que le site est accessible
- Inspectez le code HTML (la structure peut avoir changé)
- Adaptez les sélecteurs CSS dans les fonctions

### Le dashboard ne charge pas les données

- Vérifiez que `data/donnees_marche_emploi.csv` existe
- Utilisez les données d'exemple : `cp examples/donnees_emploi_echantillon.csv data/donnees_marche_emploi.csv`
- Vérifiez le format des colonnes dans le CSV
- Consultez les messages d'erreur dans le terminal

### Erreurs d'importation

- Vérifiez que toutes les dépendances sont installées
- Réinstallez les packages : `pip install -r requirements.txt --upgrade`
- Vérifiez que vous êtes dans le bon environnement virtuel

Pour plus de détails, consultez la section [Résolution de Problèmes](GUIDE_UTILISATION.md#-résolution-de-problèmes) du guide.

## Contributions

Ce projet est éducatif et ouvert aux améliorations ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Améliorer la documentation
- Ajouter de nouvelles fonctionnalités

## Ressources

### Documentation Officielle

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [Requests Documentation](https://requests.readthedocs.io/)

### Tutoriels et Guides

- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)
- [Streamlit Tutorial](https://docs.streamlit.io/get-started/tutorials/create-an-app)
- [Pandas Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)

### Ressources Pédagogiques

- [Python Web Scraping Guide](https://realpython.com/python-web-scraping-practical-introduction/)
- [Data Visualization with Plotly](https://plotly.com/python/)

## Licence

Ce projet est à des fins éducatives uniquement.
