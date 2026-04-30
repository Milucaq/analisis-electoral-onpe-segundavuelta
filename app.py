import streamlit as st
import pandas as pd

# CONFIG
st.set_page_config(page_title="Resultados ONPE 2021", layout="wide")
st.title("Resultados Electorales ONPE 2021")

# ==============================
# CARGAR DATOS DESDE GITHUB
# ==============================

@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
    
    return pd.read_csv(
        url,
        sep=";",              # MUY IMPORTANTE
        encoding="latin1",
        engine="python"
    )

df = cargar_datos()

# ==============================
# VISTA GENERAL
# ==============================

st.subheader("Vista general del dataset")
st.dataframe(df.head())

# ==============================
# DETECTAR DEPARTAMENTO
# ==============================

posibles_columnas = [col for col in df.columns if "DEPART" in col.upper()]

if len(posibles_columnas) > 0:
    columna_departamento = posibles_columnas[0]
else:
    columna_departamento = df.columns[0]

# ==============================
# FILTRO
# ==============================

departamentos = df[columna_departamento].dropna().unique()

depto_seleccionado = st.selectbox(
    "Selecciona un departamento:",
    sorted(departamentos)
)

df_filtrado = df[df[columna_departamento] == depto_seleccionado]

# ==============================
# TABLA
# ==============================

st.subheader(f"Datos del departamento: {depto_seleccionado}")
st.dataframe(df_filtrado)

# ==============================
# GRÁFICO
# ==============================

st.subheader("Visualización de datos")

columnas_numericas = df_filtrado.select_dtypes(include=["int64", "float64"]).columns

if len(columnas_numericas) > 0:
    columna_grafico = st.selectbox(
        "Selecciona columna para graficar:",
        columnas_numericas
    )

    st.bar_chart(df_filtrado[columna_grafico])
else:
    st.warning("No hay columnas numéricas para graficar")

# ==============================
# RESUMEN
# ==============================

st.subheader("Resumen estadístico")
st.write(df_filtrado.describe())
