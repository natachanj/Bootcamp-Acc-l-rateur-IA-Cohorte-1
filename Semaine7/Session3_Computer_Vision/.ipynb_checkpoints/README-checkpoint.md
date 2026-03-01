# Detection de Pneumonie par Radiographie Thoracique

> Une IA qui analyse une radiographie thoracique et predit si le patient est **Normal** ou atteint de **Pneumonie**.

---

## Description du projet

Ce projet pedagogique couvre l'ensemble du pipeline de classification d'images medicales, du Machine Learning classique au Deep Learning avance :

| Etape | Modele | Description |
|-------|--------|-------------|
| **Baseline** | Regression Logistique + PCA | ML classique sur images aplaties |
| **Deep Learning** | CNN from Scratch | Reseau convolutif construit de zero |
| **Transfer Learning** | MobileNetV2 (gele) | Backbone pre-entraine sur ImageNet |
| **Fine-Tuning** | MobileNetV2 (degele) | Adaptation des dernieres couches |

---

## Structure du projet

```
pneumonia-detection/
|
|-- data/                              <-- Dataset (non inclus, voir ci-dessous)
|   |-- chest_xray/
|   |   |-- train/
|   |   |   |-- NORMAL/
|   |   |   |-- PNEUMONIA/
|   |   |-- val/
|   |   |   |-- NORMAL/
|   |   |   |-- PNEUMONIA/
|   |   |-- test/
|   |       |-- NORMAL/
|   |       |-- PNEUMONIA/
|   |-- train/
|   |-- val/
|   |-- test/
|
|-- Pneumonia_Detection_Complet.ipynb  <-- Notebook principal
|-- requirements.txt                   <-- Dependances Python
|-- README.md                          <-- Ce fichier
|-- pneumonia_detector_finetuned.keras <-- Modele sauvegarde (genere apres execution)
```

---

## Telecharger le dataset

Le dataset **Chest X-Ray Images (Pneumonia)** est disponible sur Kaggle :

https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

### Option 1 — Telechargement manuel

1. Creer un compte Kaggle si necessaire
2. Telecharger le zip depuis le lien ci-dessus
3. Extraire dans le dossier `data/` du projet

### Option 2 — Via l'API Kaggle

```bash
pip install kaggle
kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
unzip chest-xray-pneumonia.zip -d data/
```

---

## Installation — Environnement Virtuel

### Prerequis

- **Python 3.10 ou 3.11** (recommande pour TensorFlow)
- **pip** a jour

**Important** : TensorFlow 2.15-2.17 fonctionne avec Python 3.9 a 3.12. Evitez Python 3.13+ qui n'est pas encore supporte.

---

### Linux / macOS

```bash
# 1. Verifier la version de Python
python3 --version
# -> Doit afficher Python 3.10.x ou 3.11.x

# 2. Creer l'environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate

# 4. Mettre a jour pip
pip install --upgrade pip

# 5. Installer les dependances
pip install -r requirements.txt

# 6. Enregistrer le kernel Jupyter
python -m ipykernel install --user --name=pneumonia-env --display-name="Python (Pneumonia)"

# 7. Lancer Jupyter
jupyter notebook
```

---

### Windows

```powershell
# 1. Verifier la version de Python
python --version
# -> Doit afficher Python 3.10.x ou 3.11.x

# 2. Creer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
venv\Scripts\activate

# 4. Mettre a jour pip
pip install --upgrade pip

# 5. Installer les dependances
pip install -r requirements.txt

# 6. Enregistrer le kernel Jupyter
python -m ipykernel install --user --name=pneumonia-env --display-name="Python (Pneumonia)"

# 7. Lancer Jupyter
jupyter notebook
```

---

### Alternative avec Conda

```bash
# 1. Creer l'environnement
conda create -n pneumonia python=3.11 -y

# 2. Activer
conda activate pneumonia

# 3. Installer TensorFlow via pip (recommande meme avec Conda)
pip install -r requirements.txt

# 4. Kernel Jupyter
python -m ipykernel install --user --name=pneumonia-env --display-name="Python (Pneumonia)"

# 5. Lancer
jupyter notebook
```

---

## Support GPU (optionnel mais recommande)

L'entrainement est beaucoup plus rapide avec un GPU NVIDIA.

### GPU NVIDIA (CUDA)

```bash
# Verifier que le GPU est detecte
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

Si le GPU n'est pas detecte :

```bash
# Installer la version GPU de TensorFlow (incluse par defaut depuis TF 2.15)
pip install tensorflow[and-cuda]
```

Prerequis GPU : NVIDIA Driver >= 525.60, CUDA 12.x, cuDNN 8.9+

### Mac Apple Silicon (M1/M2/M3/M4)

TensorFlow fonctionne nativement sur Apple Silicon depuis TF 2.13 :

```bash
pip install tensorflow-metal
```

---

## Utilisation

### 1. Lancer le notebook

```bash
# Activer l'environnement
source venv/bin/activate          # Linux/macOS
# ou
venv\Scripts\activate             # Windows

# Lancer Jupyter
jupyter notebook Pneumonia_Detection_Complet.ipynb
```

### 2. Selectionner le bon kernel

Dans Jupyter : **Kernel > Change Kernel > Python (Pneumonia)**

### 3. Executer les cellules dans l'ordre

Le notebook est structure en 7 parties (A a G). Executez les cellules sequentiellement.

---

## Resultats attendus

| Modele | Accuracy | Recall (Pneumonia) | AUC |
|--------|----------|-------------------|-----|
| Reg. Logistique | ~85% | ~90% | ~0.90 |
| CNN from Scratch | ~88% | ~93% | ~0.93 |
| Transfer Learning | ~92% | ~95% | ~0.96 |
| Fine-Tuning | ~94% | ~97% | ~0.97 |

Les resultats exacts varient selon la seed et le hardware.

---

## Depannage

### « ModuleNotFoundError: No module named 'tensorflow' »

L'environnement virtuel n'est pas active. Relancez `source venv/bin/activate`.

### « ResourceExhaustedError (OOM) »

Memoire GPU insuffisante. Reduisez `BATCH_SIZE` (16 au lieu de 32) dans le notebook.

### « Could not find a version that satisfies the requirement tensorflow »

Votre version de Python n'est pas compatible. Verifiez avec `python --version` (besoin de 3.10 ou 3.11).

### Le notebook tourne tres lentement (CPU uniquement)

Normal sans GPU. Reduisez `EPOCHS_CNN`, `EPOCHS_TL`, `EPOCHS_FT` pour accelerer les tests, ou utilisez Google Colab.

### « No module named 'PIL' »

Installez Pillow : `pip install Pillow`

---

## Alternative : Google Colab

Si vous n'avez pas de GPU local :

1. Uploadez le notebook sur Google Drive
2. Ouvrez avec Google Colab
3. Menu **Runtime > Change runtime type > T4 GPU**
4. Uploadez le dataset ou montez votre Google Drive

---

## Ressources

- Documentation TensorFlow : https://www.tensorflow.org/tutorials
- Keras Transfer Learning Guide : https://keras.io/guides/transfer_learning/
- Dataset Kaggle : https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
- MobileNetV2 Paper : https://arxiv.org/abs/1801.04381

---

## Avertissement

Ce projet est realise dans un **cadre pedagogique**. Le modele entraine **n'est pas un dispositif medical certifie** et ne doit en aucun cas etre utilise pour poser des diagnostics medicaux reels.

---

*Projet realise dans le cadre d'une formation Data / IA.*
