import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import statsmodels.api as sm

# Configuration de la page
st.set_page_config(
    page_title="Analyse de Régression Multiple - Publicité",
    page_icon="📊",
    layout="wide"
)

# Titre principal
st.title("📊 Analyse de Régression Multiple - Impact des Budgets Publicitaires sur les Ventes")
st.markdown("---")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("data/Advertising.csv", index_col=0)
    # Nettoyer les noms de colonnes si nécessaire
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# Sidebar pour la navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Choisir une section",
    ["Vue d'ensemble", "Analyse Univariée", "Analyse Bivariée", "Corrélation", 
     "Modèle de Régression", "Métriques d'Évaluation", "Prédiction"]
)

# Section 1: Vue d'ensemble
if section == "Vue d'ensemble":
    st.header("Vue d'ensemble des données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Aperçu des données")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("Informations sur le dataset")
        st.write(f"**Nombre d'observations:** {df.shape[0]}")
        st.write(f"**Nombre de variables:** {df.shape[1]}")
        st.write(f"**Variables:** {', '.join(df.columns.tolist())}")
    
    st.subheader("Description statistique")
    st.dataframe(df.describe(), use_container_width=True)
    
    st.subheader("Vérification des valeurs manquantes")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        st.success("✅ Aucune valeur manquante détectée")
    else:
        st.warning(f"⚠️ Valeurs manquantes détectées: {missing[missing > 0].to_dict()}")

# Section 2: Analyse Univariée
elif section == "Analyse Univariée":
    st.header("Analyse Univariée")
    st.markdown("Étude de chaque variable individuellement pour comprendre leurs distributions et caractéristiques.")
    
    # Sélection de la variable
    variable = st.selectbox("Sélectionner une variable", df.columns.tolist())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Statistiques descriptives - {variable}")
        stats = df[variable].describe()
        st.dataframe(stats.to_frame().T, use_container_width=True)
        
        st.subheader(f"Histogramme - {variable}")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df[variable], bins=20, edgecolor='black', alpha=0.7)
        ax.set_xlabel(variable)
        ax.set_ylabel("Fréquence")
        ax.set_title(f"Distribution de {variable}")
        st.pyplot(fig)
    
    with col2:
        st.subheader(f"Boxplot - {variable}")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot(df[variable], vert=True)
        ax.set_ylabel(variable)
        ax.set_title(f"Boxplot de {variable}")
        st.pyplot(fig)
        
        # Détection des outliers
        Q1 = df[variable].quantile(0.25)
        Q3 = df[variable].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[variable] < lower_bound) | (df[variable] > upper_bound)]
        
        if len(outliers) > 0:
            st.warning(f"⚠️ {len(outliers)} valeur(s) atypique(s) détectée(s)")
            st.dataframe(outliers[[variable]], use_container_width=True)
        else:
            st.success("✅ Aucune valeur atypique détectée")
    
    # Tous les histogrammes ensemble
    st.subheader("Tous les histogrammes")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    for idx, col in enumerate(df.columns):
        axes[idx].hist(df[col], bins=15, edgecolor='black', alpha=0.7)
        axes[idx].set_title(f"Distribution de {col}")
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel("Fréquence")
    plt.tight_layout()
    st.pyplot(fig)
    
    # Tous les boxplots ensemble
    st.subheader("Tous les boxplots")
    fig, ax = plt.subplots(figsize=(10, 6))
    df.boxplot(ax=ax)
    ax.set_title("Boxplots de toutes les variables")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Section 3: Analyse Bivariée
elif section == "Analyse Bivariée":
    st.header("Analyse Bivariée")
    st.markdown("Étude des relations entre deux variables à l'aide de scatter plots.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        var_x = st.selectbox("Variable X", df.columns.tolist(), key="bivar_x")
    
    with col2:
        var_y = st.selectbox("Variable Y", df.columns.tolist(), key="bivar_y")
    
    if var_x != var_y:
        # Scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df[var_x], df[var_y], alpha=0.6)
        ax.set_xlabel(var_x)
        ax.set_ylabel(var_y)
        ax.set_title(f"Relation entre {var_x} et {var_y}")
        
        # Ligne de tendance
        z = np.polyfit(df[var_x], df[var_y], 1)
        p = np.poly1d(z)
        ax.plot(df[var_x], p(df[var_x]), "r--", alpha=0.8, label="Tendance linéaire")
        ax.legend()
        
        st.pyplot(fig)
        
        # Coefficient de corrélation
        correlation = df[var_x].corr(df[var_y])
        st.metric("Coefficient de corrélation", f"{correlation:.4f}")
        
        if abs(correlation) > 0.7:
            st.info("💡 Corrélation forte détectée")
        elif abs(correlation) > 0.4:
            st.info("💡 Corrélation modérée détectée")
        else:
            st.info("💡 Corrélation faible détectée")
    else:
        st.warning("⚠️ Veuillez sélectionner deux variables différentes")

# Section 4: Corrélation
elif section == "Corrélation":
    st.header("Matrice de Corrélation")
    st.markdown("Analyse des relations linéaires entre toutes les variables.")
    
    # Calcul de la matrice de corrélation
    corr_matrix = df.corr()
    
    # Affichage de la matrice sous forme de tableau
    st.subheader("Matrice de corrélation (tableau)")
    st.dataframe(corr_matrix, use_container_width=True)
    
    # Heatmap
    st.subheader("Heatmap de corrélation")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        square=True,
        ax=ax
    )
    ax.set_title("Matrice de corrélation - Heatmap")
    plt.tight_layout()
    st.pyplot(fig)
    
    # Analyse des corrélations avec la variable cible (sales)
    if 'sales' in df.columns:
        st.subheader("Corrélations avec la variable cible (Sales)")
        sales_corr = corr_matrix['sales'].sort_values(ascending=False)
        sales_corr = sales_corr[sales_corr.index != 'sales']  # Exclure sales avec elle-même
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sales_corr.plot(kind='barh', ax=ax, color='steelblue')
        ax.set_xlabel("Coefficient de corrélation")
        ax.set_title("Corrélation des variables avec Sales")
        ax.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.dataframe(sales_corr.to_frame("Corrélation avec Sales"), use_container_width=True)

# Section 5: Modèle de Régression
elif section == "Modèle de Régression":
    st.header("Modèle de Régression Linéaire Multiple")
    
    # Préparation des données
    X = df[["tv", "radio", "newspaper"]]
    y = df["sales"]
    
    # Paramètres de split
    col1, col2 = st.columns(2)
    with col1:
        test_size = st.slider("Taille de l'ensemble de test (%)", 10, 40, 25) / 100
    with col2:
        random_state = st.number_input("Random state", min_value=0, max_value=100, value=42)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    st.info(f"📊 Données d'entraînement: {X_train.shape[0]} observations | Données de test: {X_test.shape[0]} observations")
    
    # Modèle scikit-learn
    st.subheader("Entraînement du modèle")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Coefficients
    st.subheader("Paramètres du modèle")
    
    coefficients_df = pd.DataFrame({
        "Variable": X.columns,
        "Coefficient": model.coef_,
        "Impact": ["Positif" if c > 0 else "Négatif" for c in model.coef_]
    })
    
    st.dataframe(coefficients_df, use_container_width=True)
    
    st.metric("Intercept (ordonnée à l'origine)", f"{model.intercept_:.4f}")
    
    # Visualisation des coefficients
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if c > 0 else 'red' for c in model.coef_]
    ax.barh(coefficients_df["Variable"], coefficients_df["Coefficient"], color=colors)
    ax.set_xlabel("Valeur du coefficient")
    ax.set_title("Coefficients du modèle de régression")
    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Modèle statsmodels pour plus de détails
    st.subheader("Résumé statistique détaillé (Statsmodels)")
    
    X_train_sm = sm.add_constant(X_train)
    X_test_sm = sm.add_constant(X_test)
    
    model_sm = sm.OLS(y_train, X_train_sm)
    results = model_sm.fit()
    
    st.text(str(results.summary()))

# Section 6: Métriques d'Évaluation
elif section == "Métriques d'Évaluation":
    st.header("Évaluation du Modèle")
    
    # Préparation des données
    X = df[["tv", "radio", "newspaper"]]
    y = df["sales"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    
    # Entraînement
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Métriques
    st.subheader("Métriques sur l'ensemble d'entraînement")
    col1, col2, col3, col4 = st.columns(4)
    
    mae_train = mean_absolute_error(y_train, y_pred_train)
    mse_train = mean_squared_error(y_train, y_pred_train)
    rmse_train = np.sqrt(mse_train)
    r2_train = r2_score(y_train, y_pred_train)
    
    with col1:
        st.metric("MAE", f"{mae_train:.4f}")
    with col2:
        st.metric("MSE", f"{mse_train:.4f}")
    with col3:
        st.metric("RMSE", f"{rmse_train:.4f}")
    with col4:
        st.metric("R²", f"{r2_train:.4f}")
    
    st.subheader("Métriques sur l'ensemble de test")
    col1, col2, col3, col4 = st.columns(4)
    
    mae_test = mean_absolute_error(y_test, y_pred_test)
    mse_test = mean_squared_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    r2_test = r2_score(y_test, y_pred_test)
    
    with col1:
        st.metric("MAE", f"{mae_test:.4f}")
    with col2:
        st.metric("MSE", f"{mse_test:.4f}")
    with col3:
        st.metric("RMSE", f"{rmse_test:.4f}")
    with col4:
        st.metric("R²", f"{r2_test:.4f}")
    
    # Tableau comparatif
    st.subheader("Comparaison Train vs Test")
    comparison_df = pd.DataFrame({
        "Métrique": ["MAE", "MSE", "RMSE", "R²"],
        "Train": [mae_train, mse_train, rmse_train, r2_train],
        "Test": [mae_test, mse_test, rmse_test, r2_test]
    })
    st.dataframe(comparison_df, use_container_width=True)
    
    # Graphique observé vs prédit
    st.subheader("Graphique Observé vs Prédit (Test)")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred_test, alpha=0.6)
    ax.plot([y_test.min(), y_test.max()], 
            [y_test.min(), y_test.max()], 
            'r--', lw=2, label="Ligne parfaite")
    ax.set_xlabel("Ventes observées")
    ax.set_ylabel("Ventes prédites")
    ax.set_title("Prédictions vs Observations")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Résidus
    st.subheader("Analyse des résidus")
    residuals = y_test - y_pred_test
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(y_pred_test, residuals, alpha=0.6)
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        ax.set_xlabel("Ventes prédites")
        ax.set_ylabel("Résidus")
        ax.set_title("Résidus vs Prédictions")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(residuals, bins=20, edgecolor='black', alpha=0.7)
        ax.set_xlabel("Résidus")
        ax.set_ylabel("Fréquence")
        ax.set_title("Distribution des résidus")
        ax.axvline(x=0, color='r', linestyle='--', linewidth=2)
        plt.tight_layout()
        st.pyplot(fig)

# Section 7: Prédiction
elif section == "Prédiction":
    st.header("🔮 Prédiction des Ventes")
    st.markdown("Utilisez le modèle entraîné pour prédire les ventes à partir des budgets publicitaires.")
    
    # Entraînement du modèle (même que précédemment)
    X = df[["tv", "radio", "newspaper"]]
    y = df["sales"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    st.subheader("Saisie des budgets publicitaires")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tv_budget = st.number_input(
            "Budget TV (en milliers)",
            min_value=0.0,
            max_value=500.0,
            value=150.0,
            step=1.0,
            help="Budget alloué à la publicité télévisée"
        )
    
    with col2:
        radio_budget = st.number_input(
            "Budget Radio (en milliers)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0,
            help="Budget alloué à la publicité radio"
        )
    
    with col3:
        newspaper_budget = st.number_input(
            "Budget Newspaper (en milliers)",
            min_value=0.0,
            max_value=150.0,
            value=10.0,
            step=1.0,
            help="Budget alloué à la publicité presse écrite"
        )
    
    # Prédiction
    if st.button("Prédire les ventes", type="primary"):
        input_data = pd.DataFrame({
            "tv": [tv_budget],
            "radio": [radio_budget],
            "newspaper": [newspaper_budget]
        })
        
        prediction = model.predict(input_data)[0]
        
        st.success(f"🎯 **Ventes prédites: {prediction:.2f} milliers d'unités**")
        
        # Détails de la prédiction
        st.subheader("Détails de la prédiction")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Budgets saisis:**")
            st.write(f"- TV: {tv_budget} milliers")
            st.write(f"- Radio: {radio_budget} milliers")
            st.write(f"- Newspaper: {newspaper_budget} milliers")
        
        with col2:
            st.markdown("**Contribution de chaque canal:**")
            contribution_tv = model.coef_[0] * tv_budget
            contribution_radio = model.coef_[1] * radio_budget
            contribution_newspaper = model.coef_[2] * newspaper_budget
            intercept = model.intercept_
            
            st.write(f"- TV: {contribution_tv:.2f}")
            st.write(f"- Radio: {contribution_radio:.2f}")
            st.write(f"- Newspaper: {contribution_newspaper:.2f}")
            st.write(f"- Intercept: {intercept:.2f}")
            st.write(f"- **Total: {prediction:.2f}**")
        
        # Visualisation de la contribution
        fig, ax = plt.subplots(figsize=(10, 6))
        contributions = [contribution_tv, contribution_radio, contribution_newspaper, intercept]
        labels = ["TV", "Radio", "Newspaper", "Intercept"]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        bars = ax.bar(labels, contributions, color=colors, alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.set_ylabel("Contribution aux ventes")
        ax.set_title("Contribution de chaque variable à la prédiction")
        ax.grid(True, alpha=0.3, axis='y')
        
        # Ajouter les valeurs sur les barres
        for bar, val in zip(bars, contributions):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.2f}',
                   ha='center', va='bottom' if height >= 0 else 'top')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Section pour prédire plusieurs valeurs
    st.markdown("---")
    st.subheader("Prédiction multiple")
    st.markdown("Téléversez un fichier CSV ou saisissez plusieurs valeurs pour obtenir plusieurs prédictions.")
    
    upload_option = st.radio(
        "Choisir une option",
        ["Saisie manuelle", "Upload fichier CSV"]
    )
    
    if upload_option == "Saisie manuelle":
        st.markdown("**Ajouter plusieurs lignes:**")
        num_rows = st.number_input("Nombre de lignes", min_value=1, max_value=10, value=3)
        
        input_rows = []
        for i in range(num_rows):
            with st.expander(f"Ligne {i+1}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    tv_val = st.number_input(f"TV {i+1}", min_value=0.0, value=100.0, key=f"tv_{i}")
                with col2:
                    radio_val = st.number_input(f"Radio {i+1}", min_value=0.0, value=20.0, key=f"radio_{i}")
                with col3:
                    newspaper_val = st.number_input(f"Newspaper {i+1}", min_value=0.0, value=10.0, key=f"newspaper_{i}")
                input_rows.append({"tv": tv_val, "radio": radio_val, "newspaper": newspaper_val})
        
        if st.button("Prédire toutes les valeurs"):
            input_df = pd.DataFrame(input_rows)
            predictions = model.predict(input_df)
            
            result_df = input_df.copy()
            result_df["Ventes prédites"] = predictions
            
            st.subheader("Résultats des prédictions")
            st.dataframe(result_df, use_container_width=True)
            
            # Graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            x_pos = np.arange(len(predictions))
            ax.bar(x_pos, predictions, alpha=0.7, color='steelblue')
            ax.set_xlabel("Ligne")
            ax.set_ylabel("Ventes prédites")
            ax.set_title("Prédictions multiples")
            ax.set_xticks(x_pos)
            ax.set_xticklabels([f"Ligne {i+1}" for i in range(len(predictions))])
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            st.pyplot(fig)
    
    else:
        uploaded_file = st.file_uploader("Choisir un fichier CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                upload_df = pd.read_csv(uploaded_file)
                
                # Vérifier les colonnes
                required_cols = ["tv", "radio", "newspaper"]
                missing_cols = [col for col in required_cols if col not in upload_df.columns]
                
                if missing_cols:
                    st.error(f"❌ Colonnes manquantes: {', '.join(missing_cols)}")
                    st.info("Le fichier doit contenir les colonnes: tv, radio, newspaper")
                else:
                    st.success("✅ Fichier chargé avec succès")
                    st.dataframe(upload_df[required_cols], use_container_width=True)
                    
                    if st.button("Prédire"):
                        predictions = model.predict(upload_df[required_cols])
                        
                        result_df = upload_df.copy()
                        result_df["Ventes prédites"] = predictions
                        
                        st.subheader("Résultats des prédictions")
                        st.dataframe(result_df, use_container_width=True)
                        
                        # Télécharger les résultats
                        csv = result_df.to_csv(index=False)
                        st.download_button(
                            label="Télécharger les résultats (CSV)",
                            data=csv,
                            file_name="predictions.csv",
                            mime="text/csv"
                        )
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Application créée pour l'analyse de régression multiple - Impact des budgets publicitaires sur les ventes**")

