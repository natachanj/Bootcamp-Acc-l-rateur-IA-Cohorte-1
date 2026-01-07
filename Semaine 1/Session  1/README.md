# Session 1 : Software 1.0, Programmation avec l'IA

Liens :
- [Exemple 1 : Scraping d'un tableau d'emplois IA avec Python](https://github.com/ShawhinT/AI-Builders-Bootcamp-7/blob/main/session-1/example_1-scrape_job_board.ipynb)
- [Exemple 2 : Tableau de bord d'emplois IA avec Streamlit (Vibe Coded)](https://github.com/ShawhinT/AI-Builders-Bootcamp-7/blob/main/session-1/example_2-job_dashboard.py)
- [Exemples de Live Coding](https://github.com/ShawhinT/AI-Builders-Bootcamp-7/tree/main/session-1/live-coding-example)

## Comment exécuter les exemples

### uv

1. Cloner ce dépôt
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-7.git
    ```
2. Naviguer vers le dossier téléchargé et créer un nouvel environnement virtuel
    ```
    uv sync
    ```
3. Lancer Jupyter Lab
    ```
    uv run jupyter lab
    ```

### Python standard

1. Cloner ce dépôt
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-7.git
    ```
2. Naviguer vers le dossier téléchargé et créer un nouvel environnement virtuel
    ```
    python -m venv s1-env
    ```
3. Activer l'environnement virtuel
    ```
    # mac/linux
    source s1-env/bin/activate

    # windows
    .\s1-env\Scripts\activate.bat
    ```
4. Installer les dépendances
    ```
    pip install -r requirements.txt
    ```
5. Lancer Jupyter Lab
    ```
    jupyter lab
    ```
