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
# DETECTAR COLUMNAS
# ==============================
def buscar_col(palabra):
    for col in df.columns:
        if palabra in col.upper():
            return col
    return None

col_dep = buscar_col("DEPART")
col_prov = buscar_col("PROV")
col_dist = buscar_col("DIST")
col_validos = buscar_col("VALID")
col_nulos = buscar_col("NULO")
col_blancos = buscar_col("BLANCO")

# ==============================
# FILTROS
# ==============================
st.sidebar.header("🔎 Filtros")

if col_dep:
    dep_sel = st.sidebar.selectbox("Departamento", ["Todos"] + sorted(df[col_dep].dropna().unique().tolist()))
    if dep_sel != "Todos":
        df = df[df[col_dep] == dep_sel]

if col_prov:
    prov_sel = st.sidebar.selectbox("Provincia", ["Todos"] + sorted(df[col_prov].dropna().unique().tolist()))
    if prov_sel != "Todos":
        df = df[df[col_prov] == prov_sel]

if col_dist:
    dist_sel = st.sidebar.selectbox("Distrito", ["Todos"] + sorted(df[col_dist].dropna().unique().tolist()))
    if dist_sel != "Todos":
        df = df[df[col_dist] == dist_sel]

# ==============================
# LIMPIEZA DE DATOS
# ==============================
df_limpio = df.copy()

for col in [col_validos, col_nulos, col_blancos]:
    if col:
        df_limpio[col] = pd.to_numeric(df_limpio[col], errors="coerce").fillna(0)

# ==============================
# KPI PRINCIPALES
# ==============================
st.subheader("📌 Indicadores")

total_mesas = len(df)
total_validos = df_limpio[col_validos].sum() if col_validos else 0
total_nulos = df_limpio[col_nulos].sum() if col_nulos else 0
total_blancos = df_limpio[col_blancos].sum() if col_blancos else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mesas", total_mesas)
c2.metric("Votos válidos", int(total_validos))
c3.metric("Nulos", int(total_nulos))
c4.metric("Blancos", int(total_blancos))

# ==============================
# GRÁFICO PRINCIPAL
# ==============================
st.subheader("📊 Distribución de votos")

df_graf = pd.DataFrame({
    "Tipo": ["Válidos", "Nulos", "Blancos"],
    "Cantidad": [total_validos, total_nulos, total_blancos]
}).set_index("Tipo")

st.bar_chart(df_graf)

# ==============================
# ANTES VS DESPUÉS
# ==============================
st.subheader("⚖️ Comparación antes vs después")

validos_antes = df[col_validos].fillna(0).sum() if col_validos else 0
validos_despues = df_limpio[col_validos].sum() if col_validos else 0

df_comp = pd.DataFrame({
    "Estado": ["Antes", "Después"],
    "Votos válidos": [validos_antes, validos_despues]
}).set_index("Estado")

st.bar_chart(df_comp)

# ==============================
# VOTOS POR DEPARTAMENTO
# ==============================
if col_dep and col_validos:
    st.subheader("🏆 Votos por departamento")

    votos_dep = df_limpio.groupby(col_dep)[col_validos].sum().sort_values(ascending=False)

    st.bar_chart(votos_dep)

    st.subheader("Top departamentos con más votos")
    st.dataframe(votos_dep.head(10))

# ==============================
# TABLA
# ==============================
st.subheader("📋 Datos")
st.dataframe(df.head(500))

# ==============================
# RESUMEN
# ==============================
st.subheader("📈 Estadísticas")
st.write(df_limpio.describe())
