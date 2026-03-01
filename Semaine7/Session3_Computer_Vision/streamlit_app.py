import os

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image as keras_image


MODEL_PATH = "pneumonia_detector_finetuned.keras"
IMG_SIZE = 224
CLASSES = ["NORMAL", "PNEUMONIA"]


@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Le fichier de modele '{MODEL_PATH}' est introuvable. "
            "Assure-toi d'avoir bien execute le notebook et genere le modele."
        )
    return keras.models.load_model(MODEL_PATH)


def preprocess_image(pil_img, img_size=IMG_SIZE):
    pil_img = pil_img.convert("RGB").resize((img_size, img_size))
    img_array = keras_image.img_to_array(pil_img) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    return img_batch


def predict_pneumonia(pil_img, model, threshold: float = 0.5):
    batch = preprocess_image(pil_img)
    proba = model.predict(batch, verbose=0)[0][0]
    pred_class = "PNEUMONIA" if proba >= threshold else "NORMAL"
    confidence = proba if pred_class == "PNEUMONIA" else 1 - proba
    proba_pneumonia = float(proba)
    proba_normal = float(1.0 - proba)
    return pred_class, confidence, proba_pneumonia, proba_normal


def inject_global_styles():
    st.markdown(
        """
        <style>
        .main {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }
        h1, h2, h3, h4 {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                         system-ui, "Segoe UI", sans-serif;
        }
        .stMetric {
            background-color: #ffffff;
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Détection de Pneumonie sur Radio Thoracique",
        page_icon="🩻",
        layout="wide",
    )

    inject_global_styles()

    st.title("🩻 Détection de Pneumonie sur Radio Thoracique")
    st.markdown(
        """
        **Charge une radio thoracique (JPG/PNG)** et laisse le modèle estimer la probabilité de
        pneumonie. L’objectif est pédagogique : interprète toujours le résultat avec un professionnel de santé.
        """
    )

    # Sidebar
    st.sidebar.header("À propos du modèle")
    st.sidebar.write(
        "- Architecture : **MobileNetV2 (Transfer Learning)**\n"
        f"- Taille d'entrée : **{IMG_SIZE}×{IMG_SIZE} RGB**\n"
        "- Sortie : probabilité de **PNEUMONIA** (binaire)\n"
    )
    st.sidebar.markdown("### Paramétrage")
    threshold_percent = st.sidebar.slider(
        "Seuil de décision (PNEUMONIA) en %",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.01,
        help="Au‑dessus de ce seuil (en %), l'image est classée comme PNEUMONIA.",
    )
    threshold_ratio = threshold_percent / 100.0
    st.sidebar.caption(f"Seuil actuel : **{threshold_percent:.2f}%**")

    st.sidebar.markdown("### Historique de la session")
    history = st.session_state.get("history", [])
    if history:
        st.sidebar.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    else:
        st.sidebar.caption("Aucune prédiction effectuée pour l’instant.")

    tab_pred, tab_details = st.tabs(["🧪 Prédiction", "ℹ️ Détails & interprétation"])

    with tab_pred:
        uploaded_file = st.file_uploader(
            "Glisse-dépose une image de radio thoracique ou clique pour en sélectionner une.",
            type=["png", "jpg", "jpeg"],
        )

        if uploaded_file is None:
            st.info(
                "Commence par **importer une image** de radio thoracique au format JPG ou PNG "
                "pour obtenir une prédiction."
            )
            if "last_file" in st.session_state:
                del st.session_state["last_file"]
                del st.session_state["last_proba"]
        else:
            col1, col2 = st.columns([1, 1])
            image = Image.open(uploaded_file)

            with col1:
                st.subheader("Image chargée")
                st.image(image, use_container_width=True)

            # Exécuter le modèle uniquement pour un NOUVEAU fichier
            file_id = uploaded_file.name + str(uploaded_file.size)
            if st.session_state.get("last_file") != file_id:
                with st.spinner("Chargement du modèle et calcul de la probabilité..."):
                    try:
                        model = load_model()
                        proba_pneumonia = float(
                            model.predict(preprocess_image(image), verbose=0)[0][0]
                        )
                        st.session_state["last_file"] = file_id
                        st.session_state["last_proba"] = proba_pneumonia

                        if "history" not in st.session_state:
                            st.session_state["history"] = []
                        st.session_state["history"].insert(
                            0,
                            {
                                "Fichier": uploaded_file.name,
                                "P(PNEUMONIA)": f"{proba_pneumonia:.1%}",
                            },
                        )
                        st.session_state["history"] = st.session_state["history"][:10]
                    except Exception as e:
                        st.error(
                            "Erreur lors du chargement du modèle ou de la prédiction : "
                            f"{e}"
                        )
                        return

            proba_pneumonia = st.session_state["last_proba"]
            proba_normal = 1.0 - proba_pneumonia

            # Classification dynamique selon le seuil (sans relancer le modèle)
            pred_class = "PNEUMONIA" if proba_pneumonia >= threshold_ratio else "NORMAL"
            confidence = (
                proba_pneumonia if pred_class == "PNEUMONIA" else proba_normal
            )

            with col2:
                st.subheader("Résultat du modèle")
                st.caption(
                    f"Avec seuil = **{threshold_percent:.2f}%** → classification : **{pred_class}**"
                )

                # Jauge dynamique : probabilité vs seuil
                st.markdown(
                    f"""
                    <div style="margin:0.5rem 0 1rem;">
                        <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.25rem;">
                            P(PNEUMONIA) = {proba_pneumonia:.1%} &nbsp;|&nbsp; Seuil = {threshold_percent:.2f}%
                        </div>
                        <div style="position:relative;height:24px;background:#e2e8f0;border-radius:12px;overflow:visible;">
                            <div style="position:absolute;left:0;top:0;height:100%;width:{proba_pneumonia*100}%;background:linear-gradient(90deg,#f87171,#ef4444);border-radius:12px;"></div>
                            <div style="position:absolute;left:{threshold_ratio*100}%;top:-4px;width:3px;height:32px;background:#1e293b;border-radius:2px;transform:translateX(-50%);box-shadow:0 1px 3px rgba(0,0,0,0.2);" title="Seuil"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#94a3b8;margin-top:0.2rem;">
                            <span>0% NORMAL</span>
                            <span>100% PNEUMONIA</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Carte de résultat principale
                if pred_class == "PNEUMONIA":
                    st.markdown(
                        f"""
                        <div style="padding:1rem;border-radius:0.75rem;background-color:#ffe6e6;border:1px solid #ff4b4b;">
                            <h3 style="margin:0;">🔴 Suspicion de <strong>PNEUMONIA</strong></h3>
                            <p style="margin:0.5rem 0 0;">Confiance du modèle : <strong>{confidence:.1%}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="padding:1rem;border-radius:0.75rem;background-color:#e6ffed;border:1px solid #2ecc71;">
                            <h3 style="margin:0;">🟢 Aspect <strong>NORMAL</strong></h3>
                            <p style="margin:0.5rem 0 0;">Confiance du modèle : <strong>{confidence:.1%}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("#### Probabilités détaillées")
                mcol1, mcol2 = st.columns(2)
                with mcol1:
                    st.metric("Probabilité PNEUMONIA", f"{proba_pneumonia:.1%}")
                    st.progress(float(proba_pneumonia))
                with mcol2:
                    st.metric("Probabilité NORMAL", f"{proba_normal:.1%}")
                    st.progress(float(proba_normal))

                st.caption(
                    "⚠️ Cette application est un **prototype pédagogique**. "
                    "Elle ne constitue pas un dispositif médical et ne remplace en aucun cas "
                    "l’avis d’un médecin ou d’un radiologue."
                )

    with tab_details:
        st.subheader("Comment interpréter les résultats ?")
        st.markdown(
            """
            - **NORMAL** : l’image ne présente pas de motifs typiques d’une pneumonie pour le modèle.\n
            - **PNEUMONIA** : le modèle détecte des motifs compatibles avec une pneumonie sur la radio.\n
            - **Confiance** : plus la valeur est élevée, plus le modèle est sûr de sa prédiction,
              mais il peut se tromper (bruit, mauvaise qualité d’image, cas atypiques, etc.).

            **Important :** ce projet a été conçu dans un cadre de formation en IA.  
            Il ne doit pas être utilisé pour poser un diagnostic réel.
            """
        )


if __name__ == "__main__":
    main()

