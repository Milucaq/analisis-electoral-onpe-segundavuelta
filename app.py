import streamlit as st
import pandas as pd

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="ONPE 2021 Dashboard", layout="wide")
st.title("📊 Resultados Electorales ONPE 2021")

# ==============================
# CARGAR DATA
# ==============================
@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
    return pd.read_csv(url, sep=";", encoding="latin1")

df = cargar_datos()

# ==============================
# LIMPIEZA
# ==============================
columnas_votos = ["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN", "VOTOS_VI"]

for col in columnas_votos:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ==============================
# FILTROS
# ==============================
st.sidebar.header("Filtros")

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
st.subheader("📌 Indicadores")

total_mesas = df["MESA_DE_VOTACION"].nunique()
votos_p1 = df["VOTOS_P1"].sum()
votos_p2 = df["VOTOS_P2"].sum()

votos_validos = votos_p1 + votos_p2
votos_nulos = df["VOTOS_VN"].sum()
votos_blancos = df["VOTOS_VB"].sum()

ganador = "P1" if votos_p1 > votos_p2 else "P2"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mesas", total_mesas)
c2.metric("Votos válidos", int(votos_validos))
c3.metric("Nulos", int(votos_nulos))
c4.metric("Blancos", int(votos_blancos))

st.success(f"🏆 Ganador: {ganador}")

# ==============================
# % VOTOS
# ==============================
st.subheader("📊 Porcentaje de votos")

total_general = votos_validos + votos_nulos + votos_blancos

df_porcentaje = pd.DataFrame({
    "Tipo": ["P1", "P2", "Nulos", "Blancos"],
    "Votos": [votos_p1, votos_p2, votos_nulos, votos_blancos]
})

df_porcentaje["%"] = (df_porcentaje["Votos"] / total_general) * 100

st.dataframe(df_porcentaje)

st.bar_chart(df_porcentaje.set_index("Tipo")["Votos"])

# ==============================
# VOTOS POR DEPARTAMENTO
# ==============================
st.subheader("🏆 Votos por departamento")

votos_dep = df.groupby("DEPARTAMENTO")[["VOTOS_P1", "VOTOS_P2"]].sum()

st.bar_chart(votos_dep)

# ==============================
# QUIÉN GANÓ POR DEPARTAMENTO
# ==============================
st.subheader("🗳 Ganador por departamento")

votos_dep["GANADOR"] = votos_dep.apply(lambda x: "P1" if x["VOTOS_P1"] > x["VOTOS_P2"] else "P2", axis=1)

st.dataframe(votos_dep.sort_values("VOTOS_P1", ascending=False))

# ==============================
# PARTE 2 - ANTES VS DESPUÉS
# ==============================
st.subheader("⚖️ Antes vs Después (limpieza)")

# Antes
antes_validos = df["VOTOS_P1"].sum() + df["VOTOS_P2"].sum()

# Después (ya limpio)
despues_validos = votos_validos

df_comp = pd.DataFrame({
    "Estado": ["Antes", "Después"],
    "Votos válidos": [antes_validos, despues_validos]
}).set_index("Estado")

st.bar_chart(df_comp)

# ==============================
# TABLA
# ==============================
st.subheader("📋 Datos")
st.dataframe(df.head(300))
