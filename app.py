import streamlit as st
import pandas as pd

# ==============================
# CONFIGURACIÓN
# ==============================
st.set_page_config(page_title="Dashboard ONPE 2021", layout="wide")
st.title("📊 Dashboard Electoral ONPE 2021")

# ==============================
# CARGAR DATOS DESDE GITHUB
# ==============================
@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
    return pd.read_csv(url, sep=";", encoding="latin1", engine="python")

df = cargar_datos()

# ==============================
# DETECTAR COLUMNAS CLAVE
# ==============================
def buscar_col(palabra):
    cols = [c for c in df.columns if palabra in c.upper()]
    return cols[0] if cols else None

col_dep = buscar_col("DEPART")
col_prov = buscar_col("PROV")
col_dist = buscar_col("DIST")
col_votos = buscar_col("VOTO") or buscar_col("TOTAL")

# ==============================
# FILTROS
# ==============================
st.sidebar.header("🔎 Filtros")

dep_sel = st.sidebar.selectbox("Departamento", ["Todos"] + sorted(df[col_dep].dropna().unique().tolist()))

if dep_sel != "Todos":
    df = df[df[col_dep] == dep_sel]

prov_sel = st.sidebar.selectbox("Provincia", ["Todos"] + sorted(df[col_prov].dropna().unique().tolist()))

if prov_sel != "Todos":
    df = df[df[col_prov] == prov_sel]

dist_sel = st.sidebar.selectbox("Distrito", ["Todos"] + sorted(df[col_dist].dropna().unique().tolist()))

if dist_sel != "Todos":
    df = df[df[col_dist] == dist_sel]

# ==============================
# KPI PRINCIPALES
# ==============================
st.subheader("📌 Indicadores clave")

total_votos = df[col_votos].sum()

# Intentar detectar candidatos (ajustable)
posibles_candidatos = [c for c in df.columns if "VOTO" in c.upper() and c != col_votos]

ganador = "N/D"
if len(posibles_candidatos) >= 2:
    suma = df[posibles_candidatos].sum().sort_values(ascending=False)
    ganador = suma.index[0]

col1, col2 = st.columns(2)
col1.metric("🗳 Total de votos", f"{total_votos:,.0f}")
col2.metric("🏆 Ganador (estimado)", ganador)

# ==============================
# GRÁFICO DE VOTOS POR DEPARTAMENTO
# ==============================
st.subheader("📊 Votos por Departamento")

votos_dep = df.groupby(col_dep)[col_votos].sum().sort_values(ascending=False)

st.bar_chart(votos_dep)

# ==============================
# TOP DEPARTAMENTOS
# ==============================
st.subheader("🏆 Top Departamentos con más votos")

top_dep = votos_dep.head(10)
st.dataframe(top_dep)

# ==============================
# GRÁFICO DE CANDIDATOS
# ==============================
if len(posibles_candidatos) >= 2:
    st.subheader("🗳 Comparación de candidatos")

    votos_candidatos = df[posibles_candidatos].sum()
    st.bar_chart(votos_candidatos)

# ==============================
# TABLA FINAL
# ==============================
st.subheader("📋 Datos filtrados")
st.dataframe(df.head(500))

# ==============================
# RESUMEN
# ==============================
st.subheader("📈 Estadísticas")
st.write(df.describe())
import altair as alt

# ==============================
# PARTE 2: ANTES VS DESPUÉS
# ==============================

st.header("📊 Análisis de datos electorales (Antes vs Después)")

# ------------------------------
# DETECTAR COLUMNAS
# ------------------------------
def buscar_col(palabra):
    cols = [c for c in df.columns if palabra in c.upper()]
    return cols[0] if cols else None

col_validos = buscar_col("VALID")
col_nulos = buscar_col("NULO")
col_blancos = buscar_col("BLANCO")

# ------------------------------
# ANTES DE LIMPIEZA
# ------------------------------
st.subheader("🟥 Antes de la limpieza")

df_antes = df.copy()

for col in [col_validos, col_nulos, col_blancos]:
    if col:
        df_antes[col] = pd.to_numeric(df_antes[col], errors="coerce")

validos_antes = df_antes[col_validos].sum() if col_validos else 0
nulos_antes = df_antes[col_nulos].sum() if col_nulos else 0
blancos_antes = df_antes[col_blancos].sum() if col_blancos else 0

data_antes = pd.DataFrame({
    "Tipo": ["Válidos", "Nulos", "Blancos"],
    "Cantidad": [validos_antes, nulos_antes, blancos_antes]
})

# 📊 BARRAS (ANTES)
st.write("Gráfico de barras (Antes)")
st.bar_chart(data_antes.set_index("Tipo"))

# 🥧 PIE (ANTES) con Altair
st.write("Gráfico circular (Antes)")
pie_antes = alt.Chart(data_antes).mark_arc().encode(
    theta="Cantidad",
    color="Tipo",
    tooltip=["Tipo", "Cantidad"]
)
st.altair_chart(pie_antes, use_container_width=True)

# ------------------------------
# LIMPIEZA DE DATOS
# ------------------------------
st.subheader("🧹 Limpieza de datos")

df_despues = df.copy()

for col in [col_validos, col_nulos, col_blancos]:
    if col:
        df_despues[col] = pd.to_numeric(df_despues[col], errors="coerce").fillna(0)

# ------------------------------
# DESPUÉS DE LIMPIEZA
# ------------------------------
st.subheader("🟩 Después de la limpieza")

validos_despues = df_despues[col_validos].sum() if col_validos else 0
nulos_despues = df_despues[col_nulos].sum() if col_nulos else 0
blancos_despues = df_despues[col_blancos].sum() if col_blancos else 0

data_despues = pd.DataFrame({
    "Tipo": ["Válidos", "Nulos", "Blancos"],
    "Cantidad": [validos_despues, nulos_despues, blancos_despues]
})

# 📊 BARRAS (DESPUÉS)
st.write("Gráfico de barras (Después)")
st.bar_chart(data_despues.set_index("Tipo"))

# 🥧 PIE (DESPUÉS)
st.write("Gráfico circular (Después)")
pie_despues = alt.Chart(data_despues).mark_arc().encode(
    theta="Cantidad",
    color="Tipo",
    tooltip=["Tipo", "Cantidad"]
)
st.altair_chart(pie_despues, use_container_width=True)
