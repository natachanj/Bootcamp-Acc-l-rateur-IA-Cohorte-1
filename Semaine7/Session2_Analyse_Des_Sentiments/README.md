# 🛒 Analyse de Sentiments des Avis Amazon par Deep Learning

## Problématique

> **Comment peut-on classifier automatiquement le sentiment (positif / négatif) exprimé dans les avis clients de l'application Amazon à l'aide de techniques de Deep Learning ?**

Les avis en ligne jouent un rôle crucial dans la prise de décision des consommateurs et dans la stratégie des entreprises. Ce projet développe et compare **trois architectures de Deep Learning** — ANN, RNN et LSTM — pour automatiser la classification de sentiments à partir de textes bruts.

---

## Installation

### Prérequis

- **Python 3.10+**
- [Anaconda](https://www.anaconda.com/download) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommandé)

---

## Environnement virtuel

Choisir **une** des options suivantes pour créer et activer l'environnement, puis installer les dépendances.

### Option 1 : Conda (recommandé)

```bash
# Créer l'environnement virtuel
conda create -n sentiment-analysis python=3.10 -y

# Activer l'environnement
conda activate sentiment-analysis

# Installer les dépendances
pip install -r requirements.txt

# Ajouter le kernel Jupyter
python -m ipykernel install --user --name sentiment-analysis --display-name "Python (Sentiment Analysis)"
```

### Option 2 : pip + venv

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Option 3 : Google Colab

1. Uploader le notebook sur [Google Colab](https://colab.research.google.com/)
2. Créer un dossier `data/` et y uploader les 4 fichiers CSV
3. Exécuter directement (TensorFlow est préinstallé)

---

## Structure du Projet

```
📂 DeepLearning/
├── 📄 analyse_sentiments_deep_learning.ipynb   # Notebook principal
├── 📄 requirements.txt                         # Dépendances Python
├── 📄 README.md
└── 📂 data/                                    # Données
    ├── reviews_raw.csv                         # Avis bruts (export Google Play)
    ├── reviews_clean.csv                       # Avis nettoyés
    ├── reviews_labelled.csv                    # Avis labellisés (+1 / -1)
    └── reviews_post-processing.csv             # Textes après pré-traitement NLP
```

---

## Structure des données

Les fichiers CSV peuvent se trouver dans le **répertoire courant** ou dans le sous-dossier **`data/`**. Le notebook les charge automatiquement via la fonction `load_csv()`.

### Fichiers et colonnes

| Fichier | Description | Colonnes | Utilisation |
|---------|-------------|----------|-------------|
| `reviews_raw.csv` | Données brutes (Google Play Store) | `reviewId`, `userName`, `userImage`, `content`, `score`, `thumbsUpCount`, `reviewCreatedVersion`, `at`, `replyContent`, `repliedAt` | Source initiale |
| `reviews_clean.csv` | Avis nettoyés (sans métadonnées) | `content` (texte), `score` (1–5) | EDA, chargement initial |
| `reviews_labelled.csv` | Avis avec sentiment binaire | `content`, `score`, `sentiment` (-1 ou +1) | EDA, distributions, visualisations |
| `reviews_post-processing.csv` | Textes pré-traités (lemmatisés, sans ponctuation) | `content`, `sentiment` | ML (TF-IDF) et Deep Learning (ANN, RNN, LSTM) |

### Règles de labellisation

- **Score 1–2** → sentiment **négatif** (`sentiment = -1`)
- **Score 4–5** → sentiment **positif** (`sentiment = +1`)
- **Score 3** → considéré **négatif** (`sentiment = -1`)

### Statistiques du jeu de données

- **2 147 avis** (application Amazon Shopping, Google Play Store)
- **1 253 négatifs** (-1) — 58,4 %
- **894 positifs** (+1) — 41,6 %

---

## Modèles Implémentés

### Machine Learning Classique (Baseline avec TF-IDF)

| Classifieur | Description |
|-------------|-------------|
| Bernoulli Naïve Bayes | Adapté aux features binaires |
| Multinomial Naïve Bayes | Adapté aux comptages de mots |
| Gaussian Naïve Bayes | Suppose une distribution gaussienne |
| SVM (noyau RBF) | Séparation non-linéaire |
| Arbre de Décision | Modèle interprétable |
| Forêt Aléatoire | Ensemble d'arbres de décision |
| Régression Logistique | Classificateur linéaire |

### Deep Learning

| Modèle | Architecture | Description |
|--------|-------------|-------------|
| **ANN** | Embedding → GlobalAveragePooling → Dense | Réseau dense, ne capture pas l'ordre des mots |
| **RNN** | Embedding → SimpleRNN → Dense | Capture les dépendances séquentielles |
| **LSTM** | Embedding → Bidirectional LSTM → Dense | Mémoire à long terme, lecture bidirectionnelle |

---

## Lancement

```bash
conda activate sentiment-analysis
jupyter notebook
```

Ouvrir `analyse_sentiments_deep_learning.ipynb` et sélectionner le kernel **"Python (Sentiment Analysis)"**.

> **Note** : Les fichiers CSV doivent se trouver dans le **même répertoire** que le notebook ou dans un sous-dossier `data/`. Le notebook gère les deux cas automatiquement.

---

## Pipeline du Projet

```
1. Chargement des données
        ↓
2. Exploration (EDA)
   ├── Distribution des scores
   ├── Distribution des sentiments
   └── Analyse de la longueur des avis
        ↓
3. Pré-traitement NLP
   ├── Case folding
   ├── Suppression de la ponctuation
   ├── Suppression des stopwords
   ├── Lemmatisation
   └── Nuages de mots (Word Clouds)
        ↓
4. Modélisation Baseline (ML classique + TF-IDF)
        ↓
5. Modélisation Deep Learning
   ├── Tokenisation & Padding (Keras)
   ├── ANN (Artificial Neural Network)
   ├── RNN (Recurrent Neural Network)
   └── LSTM Bidirectionnel
        ↓
6. Évaluation & Comparaison
   ├── Courbes d'apprentissage
   ├── Matrices de confusion
   ├── Tableau comparatif (Accuracy, Precision, Recall, F1)
   └── Visualisations
        ↓
7. Test sur de nouveaux exemples
```

---

## Technologies

| Catégorie | Outils |
|-----------|--------|
| Langage | Python 3.10 |
| Deep Learning | TensorFlow / Keras |
| Machine Learning | Scikit-learn |
| NLP | NLTK, WordCloud |
| Data | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Environnement | Conda, Jupyter Notebook |

---

## Résultats

Les modèles sont évalués sur 4 métriques : **Accuracy**, **Precision**, **Recall** et **F1-Score**. Le notebook génère automatiquement :
- Un tableau comparatif global (ML classique vs Deep Learning)
- Des courbes d'apprentissage pour chaque modèle DL
- Des matrices de confusion
- Des graphiques comparatifs (barres horizontales, barres groupées)
