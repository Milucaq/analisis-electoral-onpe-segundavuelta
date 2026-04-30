import streamlit as st
import pandas as pd

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="ONPE 2021 Dashboard", layout="wide")
st.title("📊 Resultados Electorales ONPE 2021")

# ==============================
# CARGAR DATOS
# ==============================
@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
    return pd.read_csv(url, sep=";", encoding="latin1")

df = cargar_datos()

# ==============================
# LIMPIEZA
# ==============================
columnas = ["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN", "VOTOS_VI", "N_CVAS", "N_ELEC_HABIL"]

for col in columnas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ==============================
# FILTROS
# ==============================
st.sidebar.header("🔎 Filtros")

dep = st.sidebar.selectbox("Departamento", ["Todos"] + sorted(df["DEPARTAMENTO"].unique()))
if dep != "Todos":
    df = df[df["DEPARTAMENTO"] == dep]

prov = st.sidebar.selectbox("Provincia", ["Todos"] + sorted(df["PROVINCIA"].unique()))
if prov != "Todos":
    df = df[df["PROVINCIA"] == prov]

dist = st.sidebar.selectbox("Distrito", ["Todos"] + sorted(df["DISTRITO"].unique()))
if dist != "Todos":
    df = df[df["DISTRITO"] == dist]

# ==============================
# KPIs
# ==============================
st.subheader("📌 Indicadores clave")

mesas = df["MESA_DE_VOTACION"].nunique()
votos_p1 = df["VOTOS_P1"].sum()
votos_p2 = df["VOTOS_P2"].sum()

votos_validos = votos_p1 + votos_p2
votos_nulos = df["VOTOS_VN"].sum()
votos_blancos = df["VOTOS_VB"].sum()
votos_impugnados = df["VOTOS_VI"].sum()

ganador = "Perú Libre" if votos_p1 > votos_p2 else "Fuerza Popular"

c1, c2, c3, c4 = st.columns(4)
c1.metric("🗳 Mesas", mesas)
c2.metric("✔ Válidos", int(votos_validos))
c3.metric("❌ Nulos", int(votos_nulos))
c4.metric("⬜ Blancos", int(votos_blancos))

st.success(f"🏆 Ganador: {ganador}")

# ==============================
# PARTICIPACIÓN
# ==============================
total_votantes = df["N_CVAS"].sum()
total_habiles = df["N_ELEC_HABIL"].sum()

participacion = (total_votantes / total_habiles) * 100 if total_habiles > 0 else 0

st.info(f"👥 Participación electoral: {participacion:.2f}%")

# ==============================
# GRÁFICO PRINCIPAL
# ==============================
st.subheader("📊 Distribución de votos")

df_graf = pd.DataFrame({
    "Tipo": ["Perú Libre", "Fuerza Popular", "Nulos", "Blancos"],
    "Votos": [votos_p1, votos_p2, votos_nulos, votos_blancos]
}).set_index("Tipo")

st.bar_chart(df_graf)

# ==============================
# VOTOS POR DEPARTAMENTO
# ==============================
st.subheader("🏆 Votos por departamento")

df["TOTAL_VOTOS"] = df["VOTOS_P1"] + df["VOTOS_P2"]

votos_dep = df.groupby("DEPARTAMENTO")["TOTAL_VOTOS"].sum().sort_values(ascending=False)

st.bar_chart(votos_dep)

st.dataframe(votos_dep.head(10))

# ==============================
# GANADOR POR DEPARTAMENTO
# ==============================
st.subheader("🗳 Ganador por departamento")

ganador_dep = df.groupby("DEPARTAMENTO")[["VOTOS_P1", "VOTOS_P2"]].sum()
ganador_dep["GANADOR"] = ganador_dep.apply(
    lambda x: "Perú Libre" if x["VOTOS_P1"] > x["VOTOS_P2"] else "Fuerza Popular",
    axis=1
)

st.dataframe(ganador_dep)

# ==============================
# TABLA
# ==============================
st.subheader("📋 Datos")
st.dataframe(df.head(300))
# ==============================
# VISUALIZACIONES
# ==============================
st.header("📊 Visualización de resultados")

# ------------------------------
# 1. BARRAS - VOTOS POR CANDIDATO
# ------------------------------
st.subheader("🗳 Votos por candidato")

df_candidatos = pd.DataFrame({
    "Candidato": ["Perú Libre", "Fuerza Popular"],
    "Votos": [votos_p1, votos_p2]
}).set_index("Candidato")

st.bar_chart(df_candidatos)

# ------------------------------
# 2. DISTRIBUCIÓN POR REGIÓN
# ------------------------------
st.subheader("🌎 Distribución de votos por región")

votos_region = df.groupby("DEPARTAMENTO")[["VOTOS_P1", "VOTOS_P2"]].sum()

st.bar_chart(votos_region)

# ------------------------------
# 3. COMPARACIÓN GENERAL
# ------------------------------
st.subheader("⚖️ Comparación de resultados")

df_comparacion = pd.DataFrame({
    "Tipo": ["Perú Libre", "Fuerza Popular", "Nulos", "Blancos"],
    "Votos": [votos_p1, votos_p2, votos_nulos, votos_blancos]
}).set_index("Tipo")

st.bar_chart(df_comparacion)
# ==============================
# INTERPRETACIÓN
# ==============================
st.header("🧠 Interpretación de resultados")

# Diferencia
diferencia = abs(votos_p1 - votos_p2)

if votos_p1 > votos_p2:
    texto_ganador = "Perú Libre"
else:
    texto_ganador = "Fuerza Popular"

st.write(f"""
🔎 **Análisis general:**

- El candidato ganador es **{texto_ganador}**, con una diferencia de **{int(diferencia)} votos**.
- Se observa una clara distribución de votos a nivel nacional.
- Los votos válidos representan la mayor proporción del total.
- Los votos nulos y blancos tienen menor impacto, pero son relevantes para el análisis electoral.

📊 **Conclusión:**
Los resultados reflejan la preferencia electoral de la población en la segunda vuelta presidencial, mostrando diferencias entre regiones y una tendencia clara hacia el candidato ganador.
""")
# ==============================
# MACHINE LEARNING
# ==============================
st.header("🤖 Machine Learning aplicado")

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans

# ------------------------------
# PREPARAR DATOS
# ------------------------------
df_ml = df.copy()

# Crear variable objetivo (ganador por mesa)
df_ml["GANADOR"] = df_ml.apply(
    lambda x: 1 if x["VOTOS_P1"] > x["VOTOS_P2"] else 0, axis=1
)

# Variables predictoras
X = df_ml[["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]]
y = df_ml["GANADOR"]

# ------------------------------
# DIVISIÓN
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ------------------------------
# MODELO DE CLASIFICACIÓN
# ------------------------------
modelo = DecisionTreeClassifier(max_depth=5)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

st.subheader("📊 Clasificación: Predicción de ganador")

st.write(f"✔ Precisión del modelo: {accuracy:.2f}")

# ------------------------------
# CLUSTERING
# ------------------------------
st.subheader("📊 Agrupamiento de mesas (Clustering)")

kmeans = KMeans(n_clusters=3, random_state=42)

df_ml["CLUSTER"] = kmeans.fit_predict(X)

st.write("Distribución de clusters:")
st.bar_chart(df_ml["CLUSTER"].value_counts())

# ------------------------------
# VISUALIZACIÓN SIMPLE
# ------------------------------
st.subheader("📈 Relación entre votos y clusters")

st.scatter_chart(df_ml[["VOTOS_P1", "VOTOS_P2"]])

# ------------------------------
# INTERPRETACIÓN
# ------------------------------
st.subheader("🧠 Interpretación del modelo")

st.write(f"""
- El problema se abordó como **clasificación**, prediciendo el ganador por mesa.
- El modelo alcanzó una precisión de **{accuracy:.2f}**, lo que indica un buen ajuste.
- El clustering permitió agrupar mesas con comportamientos similares.
- Se identifican patrones de voto que diferencian regiones o tendencias electorales.
""")
