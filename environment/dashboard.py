import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import boto3
from io import StringIO

# -------------------------
# Configuration page
# -------------------------
st.set_page_config(page_title="Dashboard Météo", layout="wide")
st.title("Dashboard Météo - Quartier Montaudran")

# -------------------------
# Configuration S3
# -------------------------
BUCKET_NAME = "meteo-processed4"
PREFIX = "processed/"

# -------------------------
# Fonction pour lister et télécharger les fichiers CSV depuis S3
# -------------------------
def load_csv_from_s3(bucket_name, prefix):
    s3 = boto3.client("s3")
    dfs = []

    # Lister tous les objets dans le bucket avec le préfixe donné
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if "Contents" not in response:
        st.error("Aucun fichier trouvé dans le bucket S3.")
        st.stop()

    for obj in response["Contents"]:
        if obj["Key"].endswith(".csv"):
            try:
                # Télécharger le fichier
                file_obj = s3.get_object(Bucket=bucket_name, Key=obj["Key"])
                # Lire le contenu du fichier
                csv_content = file_obj["Body"].read().decode("utf-8")
                # Charger dans un DataFrame
                df = pd.read_csv(StringIO(csv_content), sep=";", encoding="utf-8")
                # Ajouter une colonne pour identifier la source
                df["source"] = obj["Key"].split("/")[-1]
                dfs.append(df)
            except Exception as e:
                st.warning(f"Erreur lors du chargement du fichier {obj['Key']}: {e}")

    if not dfs:
        st.error("Aucun fichier CSV valide trouvé.")
        st.stop()

    return pd.concat(dfs, ignore_index=True)

# -------------------------
# Chargement des fichiers CSV depuis S3
# -------------------------
try:
    df = load_csv_from_s3(BUCKET_NAME, PREFIX)
except Exception as e:
    st.error(f"Erreur lors du chargement des fichiers : {e}")
    st.stop()

# -------------------------
# Conversion colonnes numériques
# -------------------------
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        pass

# -------------------------
# FILTRE ANNEE MULTIPLE
# -------------------------
if "annee" in df.columns:
    annees_dispo = sorted(df["annee"].dropna().unique())

    annees_selection = st.multiselect(
        "Sélectionner une ou plusieurs années :",
        options=annees_dispo,
        default=[max(annees_dispo)]
    )

    if annees_selection:
        df = df[df["annee"].isin(annees_selection)]


# -------------------------
# Informations générales
# -------------------------
st.markdown("### Informations générales")
col1, col2 = st.columns(2)

if "temperature" in df.columns:
    temp_min = df["temperature"].min()
    temp_max = df["temperature"].max()
    with col1:
        st.metric("🌡 Température minimale", f"{temp_min:.1f} °C")
    with col2:
        st.metric("🌡 Température maximale", f"{temp_max:.1f} °C")
else:
    with col1:
        st.write("Colonne 'temperature' introuvable")
    with col2:
        st.write("")

st.divider()

# -------------------------
# Graphiques
# -------------------------
st.markdown("###  Visualisation")
col1, col2 = st.columns(2)

if "temperature" in df.columns and "mois" in df.columns and "annee" in df.columns:
    with col1:
        st.subheader("Température moyenne par mois et année")

        df_temp_grouped = (
            df.groupby(["annee", "mois"])["temperature"]
            .mean()
            .reset_index()
            .sort_values(["annee", "mois"])
        )

        df_temp_grouped["mois-annee"] = ( df_temp_grouped["mois"].astype(str)+ "-"+ df_temp_grouped["annee"].astype(str))

        st.line_chart(df_temp_grouped, x="mois", y="temperature")


if "humidite" in df.columns and "mois" in df.columns and "annee" in df.columns:
    with col2:
        st.subheader("Humidité moyenne par mois et année")

        df_hum_grouped = (
            df.groupby(["annee", "mois"])["humidite"]
            .mean()
            .reset_index()
            .sort_values(["annee", "mois"])
        )
        df_hum_grouped["mois-annee"] = ( df_hum_grouped["mois"].astype(str) + "-" + df_hum_grouped["annee"].astype(str))

        st.line_chart(df_hum_grouped, x="mois-annee", y="humidite")


st.divider()

# -------------------------
# Graphique comparatif Pression moyenne
# -------------------------
if "annee" in df.columns and "pression" in df.columns and "annees_selection" in locals():
    fig = go.Figure()
    for annee in sorted(annees_selection):
        pression_moy = df[df["annee"] == annee]["pression"].mean()
        fig.add_trace(go.Bar(
            x=[f"A-{annee}"],
            y=[pression_moy],
            name=f"{annee}"
        ))

    fig.update_layout(
        title="Pression moyenne par année",
        yaxis_title="Pression moyenne",
        xaxis_title="Année",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------
# Tableau complet
# -------------------------
st.markdown("### Données complètes")
st.dataframe(df, use_container_width=True, height=500)
