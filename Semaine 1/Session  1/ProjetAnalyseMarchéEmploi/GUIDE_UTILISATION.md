# 📖 Guide d'Utilisation Complet

> Guide détaillé pour utiliser le projet d'analyse de marché des emplois tech

## 📋 Table des Matières

- [Démarrage Rapide](#-démarrage-rapide)
- [Installation Détaillée](#-installation-détaillée)
- [Partie 1 : Scraping des Données](#-partie-1--scraping-des-données)
- [Partie 2 : Dashboard Interactif](#-partie-2--dashboard-interactif)
- [Notes Pédagogiques](#-notes-pédagogiques)
- [Exercices Suggérés](#-exercices-suggérés)
- [Résolution de Problèmes](#-résolution-de-problèmes)
- [Ressources Complémentaires](#-ressources-complémentaires)

---

## 🚀 Démarrage Rapide

### Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Python 3.8 ou supérieur installé
- ✅ Une connexion Internet active
- ✅ Un navigateur web moderne (Chrome, Firefox, Safari, Edge)

### Installation Express (3 minutes)

```bash
# 1. Installer les dépendances
uv sync
# ou
pip install -r requirements.txt

# 2. Lancer Jupyter Notebook
uv run jupyter notebook
# ou
jupyter notebook

# 3. Ouvrir le notebook Partie1-scraper_emplois.ipynb
# 4. Exécuter toutes les cellules (Shift + Enter)

# 5. Lancer le dashboard
streamlit run Partie2_tableau_bord_marche_emploi.py
```

---

## 📦 Installation Détaillée

### Étape 1 : Vérifier Python

```bash
python --version
# Doit afficher Python 3.8.x ou supérieur
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/)

### Étape 2 : Créer un environnement virtuel (Recommandé)

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances

#### Option A : Avec uv (Recommandé - Plus rapide)

```bash
# Installer uv si ce n'est pas déjà fait
pip install uv

# Installer toutes les dépendances
uv sync
```

#### Option B : Avec pip (Standard)

```bash
pip install -r requirements.txt
```

### Étape 4 : Vérifier l'installation

```bash
python -c "import pandas, streamlit, plotly, bs4; print('✅ Installation réussie !')"
```

Si vous voyez le message de succès, vous êtes prêt à commencer !

---

## 📓 Partie 1 : Scraping des Données

### Vue d'ensemble

Le notebook `Partie1-scraper_emplois.ipynb` contient tout le code nécessaire pour :

1. Scraper des offres d'emploi depuis des sites spécialisés
2. Extraire automatiquement des informations structurées
3. Nettoyer et traiter les données
4. Sauvegarder les résultats en CSV

### Structure du Notebook

Le notebook est organisé en sections :

1. **Imports et Configuration** : Bibliothèques et paramètres
2. **Fonctions Utilitaires** : Extraction intelligente de données
3. **Fonction Principale** : Scraping depuis un site spécifique
4. **Collecte des URLs** : Récupération des liens d'emplois
5. **Extraction des Détails** : Récupération des informations complètes
6. **Traitement des Données** : Nettoyage et normalisation
7. **Analyse** : Statistiques et tendances
8. **Sauvegarde** : Export en CSV

### Instructions Pas à Pas

#### 1. Ouvrir Jupyter Notebook

```bash
uv run jupyter notebook
# ou
jupyter notebook
```

Jupyter Notebook s'ouvrira dans votre navigateur par défaut.

#### 2. Ouvrir le Notebook

Dans Jupyter Notebook, naviguez vers `Partie1-scraper_emplois.ipynb` et cliquez pour l'ouvrir.

#### 3. Exécuter les Cellules

**Méthode 1 : Cellule par cellule**
- Cliquez sur une cellule
- Appuyez sur `Shift + Enter` pour exécuter
- Passez à la cellule suivante

**Méthode 2 : Tout exécuter**
- Menu : `Cell` → `Run All`
- Ou raccourci clavier : `Ctrl + Shift + Enter` (Windows/Linux) / `Cmd + Shift + Enter` (Mac)

#### 4. Comprendre les Résultats

Après l'exécution, vous verrez :

- 📊 Nombre d'emplois scrapés
- 📈 Statistiques sur les types de contrats
- 🔧 Technologies les plus recherchées
- 💰 Informations sur les salaires
- 💾 Confirmation de sauvegarde dans `data/donnees_marche_emploi.csv`

### Fonctionnalités Avancées

#### Extraction Intelligente

Le notebook utilise des fonctions pour détecter automatiquement :

- **Types de contrats** : Analyse du texte pour identifier Remote/Hybrid/On-site
- **Niveaux d'expérience** : Détection de Junior/Mid-level/Senior depuis les descriptions
- **Stack technique** : Identification des technologies mentionnées
- **Salaires** : Extraction des fourchettes salariales

#### Personnalisation

Pour adapter le scraping à un autre site :

1. **Modifier les sélecteurs CSS** dans `extract_job_details_from_aijobs()`
2. **Inspecter le HTML** du site cible avec les outils développeur
3. **Tester sur une seule page** avant de scraper en masse
4. **Adapter les fonctions utilitaires** si nécessaire

### ⚠️ Points d'Attention

#### Respect des Sites Web

- ✅ **Vérifiez robots.txt** : `https://site.com/robots.txt`
- ✅ **Délais entre requêtes** : Minimum 2 secondes (configuré dans `REQUEST_DELAY`)
- ✅ **User-Agent approprié** : Déjà configuré dans `HEADERS`
- ✅ **Respectez les limites** : Ne scrapez pas trop de pages d'un coup

#### Gestion des Erreurs

Le code inclut des `try/except` pour gérer :
- Les erreurs de connexion
- Les pages non trouvées
- Les changements de structure HTML
- Les timeouts

Si vous rencontrez des erreurs :
1. Vérifiez les messages dans la sortie du notebook
2. Inspectez le code HTML du site
3. Adaptez les sélecteurs CSS si nécessaire

---

## 🎨 Partie 2 : Dashboard Interactif

### Vue d'ensemble

Le dashboard Streamlit (`Partie2_tableau_bord_marche_emploi.py`) offre une interface web interactive pour :

- Visualiser les données scrapées
- Filtrer et rechercher des emplois
- Analyser les tendances du marché
- Exporter les données filtrées

### Lancer le Dashboard

```bash
streamlit run Partie2_tableau_bord_marche_emploi.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

### Utiliser le Dashboard

#### 1. Charger les Données

Le dashboard propose deux options :

- **📁 Données existantes** : Charge `data/donnees_marche_emploi.csv`
- **🌐 Scraping en direct** : Scrape des données directement depuis le dashboard

#### 2. Naviguer dans les Sections

Le dashboard est organisé en onglets :

- **📊 Vue d'ensemble** : Statistiques globales
- **🌍 Géographie** : Répartition par localisation
- **💼 Types de contrats** : Analyse Remote/Hybrid/On-site
- **📈 Expérience** : Distribution par niveau requis
- **🔧 Technologies** : Stack technique recherchée
- **💰 Salaires** : Analyse des rémunérations

#### 3. Utiliser les Filtres

- **Recherche textuelle** : Rechercher dans les titres, entreprises, descriptions
- **Filtres par critères** : Localisation, type de contrat, niveau d'expérience
- **Filtres par technologies** : Sélectionner les technologies recherchées

#### 4. Exporter les Données

- Cliquez sur le bouton **📥 Télécharger CSV**
- Les données filtrées seront téléchargées
- Ouvrez le fichier dans Excel, Google Sheets, ou un autre outil

### Fonctionnalités du Dashboard

#### Visualisations Interactives

- **Graphiques Plotly** : Zoom, pan, hover pour plus de détails
- **Tableaux interactifs** : Tri et filtrage dans les tableaux
- **Cartes géographiques** : Visualisation des opportunités par région

#### Analyses Disponibles

- 📊 **Statistiques globales** : Nombre total d'emplois, salaires moyens
- 🌍 **Analyse géographique** : Top villes/régions avec le plus d'opportunités
- 💼 **Types de contrats** : Pourcentage Remote vs Hybrid vs On-site
- 📈 **Niveaux d'expérience** : Distribution Junior/Mid/Senior
- 🔧 **Technologies** : Top 10 technologies les plus recherchées
- 💰 **Salaires** : Comparaison par localisation et type de contrat

### Astuces d'Utilisation

- 💡 **Combinez les filtres** : Utilisez plusieurs filtres simultanément pour des analyses précises
- 💡 **Explorez les graphiques** : Passez la souris sur les éléments pour voir les détails
- 💡 **Exportez régulièrement** : Sauvegardez vos analyses filtrées
- 💡 **Comparez les périodes** : Scrapez à différents moments pour voir l'évolution

---

## 🎓 Notes Pédagogiques

### Pour les Étudiants

Ce projet est conçu pour vous apprendre :

#### Concepts Clés

1. **Web Scraping**
   - Comprendre la structure HTML
   - Utiliser des sélecteurs CSS/XPath
   - Gérer les requêtes HTTP
   - Respecter l'éthique du scraping

2. **Traitement de Données**
   - Nettoyer des données brutes
   - Normaliser les formats
   - Gérer les valeurs manquantes
   - Transformer les données

3. **Visualisation**
   - Créer des graphiques interactifs
   - Concevoir des dashboards
   - Présenter des données de manière claire

4. **Analyse de Données**
   - Identifier des tendances
   - Faire des statistiques descriptives
   - Comparer des groupes de données

### Points d'Attention Importants

#### 1. Respect des Sites Web

- ⚠️ **Toujours vérifier robots.txt** avant de scraper
- ⚠️ **Ajouter des délais** entre les requêtes (minimum 2 secondes)
- ⚠️ **Ne pas surcharger** les serveurs
- ⚠️ **Respecter les conditions d'utilisation** des sites

#### 2. Gestion des Erreurs

- ✅ Le code inclut des `try/except` pour gérer les erreurs
- ✅ Vérifiez les messages d'erreur si quelque chose ne fonctionne pas
- ✅ Les sites peuvent changer leur structure HTML
- ✅ Adaptez les sélecteurs CSS si nécessaire

#### 3. Adaptation du Code

- 🔧 Les sélecteurs CSS/HTML doivent être adaptés selon le site
- 🔧 Inspectez le code HTML avec les outils développeur (F12)
- 🔧 Testez d'abord sur une seule page avant de scraper en masse
- 🔧 Documentez vos modifications

### Fonctionnalités Uniques de ce Projet

Ce projet se distingue par son focus sur :

- **Types de contrats** : Analyse détaillée Remote/Hybrid/On-site
- **Niveaux d'expérience** : Extraction automatique depuis les descriptions
- **Stack technique** : Détection intelligente des technologies recherchées
- **Analyse de marché** : Tendances géographiques et salariales
- **Extraction intelligente** : Utilisation de regex et NLP pour extraire des infos structurées

---

## 💡 Exercices Suggérés

### Niveau Débutant 🟢

#### Exercice 1 : Modifier les Fonctions d'Extraction

**Objectif** : Ajouter la détection d'une nouvelle information

**Tâches** :
1. Créer une fonction `extract_contract_type()` pour détecter CDI/CDD/Freelance
2. Ajouter cette fonction dans le pipeline d'extraction
3. Tester sur quelques descriptions d'emploi

**Indices** :
- Utilisez des mots-clés comme "CDI", "permanent", "freelance", "contract"
- Suivez le pattern des fonctions existantes (`detect_work_mode()`)

#### Exercice 2 : Ajouter des Technologies

**Objectif** : Étendre la liste des technologies détectées

**Tâches** :
1. Ouvrir la fonction `extract_tech_stack()`
2. Ajouter 5 nouvelles technologies à la liste `tech_keywords`
3. Tester sur des descriptions contenant ces technologies

**Exemples** : Vue.js, Svelte, Rust, Elixir, GraphQL

#### Exercice 3 : Personnaliser les Graphiques

**Objectif** : Modifier les couleurs et styles des visualisations

**Tâches** :
1. Ouvrir le dashboard Streamlit
2. Trouver les sections de création de graphiques
3. Modifier les couleurs dans les paramètres `color_discrete_map`
4. Changer les titres et labels

### Niveau Intermédiaire 🟡

#### Exercice 1 : Adapter pour un Autre Site

**Objectif** : Scraper depuis un site d'emploi différent

**Tâches** :
1. Choisir un site d'emploi tech (ex: Indeed, LinkedIn, etc.)
2. Inspecter le HTML avec les outils développeur
3. Créer une nouvelle fonction `extract_job_details_from_[site]()`
4. Adapter les sélecteurs CSS
5. Tester sur quelques pages

**Points d'attention** :
- Respectez robots.txt
- Ajoutez des délais appropriés
- Gérez les erreurs

#### Exercice 2 : Analyse de Sentiment

**Objectif** : Analyser le ton des descriptions d'emploi

**Tâches** :
1. Installer une bibliothèque de sentiment analysis (ex: `textblob` ou `vaderSentiment`)
2. Créer une fonction pour analyser le sentiment
3. Ajouter une colonne "sentiment" au DataFrame
4. Visualiser les résultats dans le dashboard

**Indices** :
```python
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # -1 à 1
```

#### Exercice 3 : Graphiques de Corrélation

**Objectif** : Créer des graphiques montrant les corrélations

**Tâches** :
1. Analyser la corrélation entre salaire et technologies
2. Créer un graphique de corrélation (heatmap)
3. Analyser la corrélation entre type de contrat et localisation
4. Ajouter ces visualisations au dashboard

**Exemples de corrélations** :
- Salaire vs Nombre de technologies requises
- Remote vs Salaires moyens
- Technologies vs Niveau d'expérience

### Niveau Avancé 🔴

#### Exercice 1 : Scraping Multi-Sites Simultané

**Objectif** : Scraper plusieurs sites en parallèle

**Tâches** :
1. Utiliser `concurrent.futures` ou `asyncio`
2. Créer des fonctions de scraping pour 2-3 sites différents
3. Exécuter le scraping en parallèle
4. Combiner les résultats

**Points d'attention** :
- Gérez les erreurs pour chaque site
- Respectez les limites de chaque site
- Normalisez les données de différents sites

#### Exercice 2 : Comparaison de Salaires par Région

**Objectif** : Créer un système de comparaison avancé

**Tâches** :
1. Extraire les villes/pays depuis les localisations
2. Calculer les salaires moyens par région
3. Créer une carte interactive avec Plotly
4. Ajouter des filtres par technologie et niveau d'expérience

**Fonctionnalités à ajouter** :
- Comparaison entre 2-3 régions
- Graphiques de distribution des salaires
- Tableaux comparatifs

#### Exercice 3 : Système de Recommandation

**Objectif** : Recommander des emplois basés sur un profil

**Tâches** :
1. Créer un formulaire pour saisir un profil utilisateur :
   - Technologies connues
   - Niveau d'expérience
   - Localisation préférée
   - Type de contrat souhaité
2. Créer un algorithme de scoring
3. Trier les emplois par score de correspondance
4. Afficher les top 10 recommandations

**Algorithme de scoring** :
- +10 points par technologie correspondante
- +20 points si niveau d'expérience correspond
- +15 points si localisation correspond
- +10 points si type de contrat correspond

---

## 🐛 Résolution de Problèmes

### Problème : Le scraping ne fonctionne pas

#### Symptômes
- Erreur de connexion
- Aucune donnée extraite
- Erreurs 403/404

#### Solutions

1. **Vérifier la connexion Internet**
   ```bash
   ping google.com
   ```

2. **Vérifier que le site est accessible**
   - Ouvrez le site dans votre navigateur
   - Vérifiez qu'il n'y a pas de maintenance

3. **Inspecter le code HTML**
   - Ouvrez les outils développeur (F12)
   - Vérifiez si la structure HTML a changé
   - Adaptez les sélecteurs CSS si nécessaire

4. **Vérifier robots.txt**
   ```bash
   curl https://site.com/robots.txt
   ```

5. **Augmenter les délais**
   - Modifiez `REQUEST_DELAY` dans le notebook
   - Essayez avec 3-5 secondes

### Problème : Le dashboard ne charge pas les données

#### Symptômes
- Message "Aucune donnée trouvée"
- Erreur de lecture du CSV
- Dashboard vide

#### Solutions

1. **Vérifier que le fichier CSV existe**
   ```bash
   ls -la data/donnees_marche_emploi.csv
   ```

2. **Utiliser les données d'exemple**
   ```bash
   cp examples/donnees_emploi_echantillon.csv data/donnees_marche_emploi.csv
   ```

3. **Vérifier le format du CSV**
   - Ouvrez le fichier dans un éditeur de texte
   - Vérifiez qu'il n'est pas vide
   - Vérifiez l'encodage (doit être UTF-8)

4. **Vérifier les colonnes requises**
   Le CSV doit contenir au minimum :
   - `job_title`
   - `company_name`
   - `location`
   - `work_mode`
   - `experience_level`

5. **Consulter les logs**
   - Regardez le terminal où Streamlit tourne
   - Cherchez les messages d'erreur

### Problème : Erreurs d'importation

#### Symptômes
- `ModuleNotFoundError`
- `ImportError`
- Packages non trouvés

#### Solutions

1. **Vérifier l'environnement virtuel**
   ```bash
   which python
   # Doit pointer vers votre venv
   ```

2. **Réinstaller les dépendances**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Vérifier l'installation**
   ```bash
   pip list | grep pandas
   pip list | grep streamlit
   ```

4. **Réinstaller un package spécifique**
   ```bash
   pip uninstall pandas
   pip install pandas
   ```

### Problème : Les données ne s'affichent pas correctement

#### Symptômes
- Graphiques vides
- Valeurs manquantes
- Format incorrect

#### Solutions

1. **Vérifier le format des colonnes**
   ```python
   import pandas as pd
   df = pd.read_csv('data/donnees_marche_emploi.csv')
   print(df.dtypes)
   print(df.head())
   ```

2. **Vérifier les valeurs manquantes**
   ```python
   print(df.isnull().sum())
   ```

3. **Nettoyer les données**
   - Remplacer les valeurs manquantes
   - Convertir les types de données
   - Normaliser les formats

4. **Vérifier les colonnes attendues**
   Assurez-vous que ces colonnes existent :
   - `job_title`, `company_name`, `location`
   - `work_mode`, `experience_level`
   - `salary_min`, `salary_max` (optionnel)
   - `tech_stack_str` (optionnel)

### Problème : Performance lente

#### Symptômes
- Scraping très lent
- Dashboard qui met du temps à charger

#### Solutions

1. **Réduire le nombre de pages scrapées**
   - Modifiez `MAX_JOBS_TO_SCRAPE`
   - Commencez avec 10-20 emplois

2. **Optimiser les requêtes**
   - Utilisez `lxml` comme parser (déjà configuré)
   - Réduisez la taille des descriptions extraites

3. **Utiliser le cache Streamlit**
   - Le dashboard utilise déjà `@st.cache_data`
   - Rechargez la page pour voir les changements

4. **Optimiser les visualisations**
   - Limitez le nombre de points sur les graphiques
   - Utilisez l'échantillonnage pour les grandes datasets

---

## 📚 Ressources Complémentaires

### Documentation Officielle

- **[BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)** : Guide complet du parsing HTML
- **[Streamlit Documentation](https://docs.streamlit.io/)** : Documentation complète de Streamlit
- **[Pandas Documentation](https://pandas.pydata.org/docs/)** : Guide de référence pour pandas
- **[Plotly Documentation](https://plotly.com/python/)** : Tous les types de graphiques disponibles
- **[Requests Documentation](https://requests.readthedocs.io/)** : Guide pour les requêtes HTTP

### Tutoriels et Guides

- **[Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)** : Bonnes pratiques du scraping
- **[Streamlit Tutorial](https://docs.streamlit.io/get-started/tutorials/create-an-app)** : Tutoriel officiel Streamlit
- **[Pandas Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)** : Tutoriels pandas pour débutants
- **[Python Web Scraping Guide](https://realpython.com/python-web-scraping-practical-introduction/)** : Guide pratique Real Python

### Ressources Pédagogiques

- **[Data Visualization with Plotly](https://plotly.com/python/)** : Exemples de visualisations
- **[BeautifulSoup Tutorial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start)** : Guide de démarrage rapide
- **[Streamlit Components](https://streamlit.io/components)** : Composants supplémentaires

### Outils Utiles

- **[Chrome DevTools](https://developer.chrome.com/docs/devtools/)** : Pour inspecter le HTML
- **[Postman](https://www.postman.com/)** : Pour tester les API
- **[Regex101](https://regex101.com/)** : Pour tester les expressions régulières
- **[JSON Formatter](https://jsonformatter.org/)** : Pour formater le JSON

---

## 💬 Support

Si vous rencontrez des problèmes non couverts dans ce guide :

1. **Consultez les messages d'erreur** : Ils contiennent souvent la solution
2. **Vérifiez la documentation** : Les liens ci-dessus sont très utiles
3. **Cherchez sur Stack Overflow** : Beaucoup de problèmes ont déjà été résolus
4. **Inspectez le code** : Le code est bien commenté pour vous aider

---

**Bon apprentissage ! 🚀**

N'hésitez pas à expérimenter et à adapter le code à vos besoins. C'est en pratiquant que l'on apprend le mieux !
