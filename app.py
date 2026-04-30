import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Resultados ONPE", layout="wide")

# Título
st.title("Resultados Electorales ONPE 2021")

# URL del dataset (RAW de GitHub)
url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv(url, encoding='latin1')

df = cargar_datos()

# Mostrar info básica
st.subheader("Vista general del dataset")
st.dataframe(df.head())

# ==============================
# FILTRO POR DEPARTAMENTO
# ==============================

# OJO: cambia el nombre de la columna si es diferente
columna_departamento = df.columns[0]  # ajustamos dinámico

departamentos = df[columna_departamento].dropna().unique()

depto_seleccionado = st.selectbox(
    "Selecciona un departamento:",
    departamentos
)

df_filtrado = df[df[columna_departamento] == depto_seleccionado]

# ==============================
# MOSTRAR DATOS FILTRADOS
# ==============================

st.subheader(f"Datos del departamento: {depto_seleccionado}")
st.dataframe(df_filtrado)

# ==============================
# GRÁFICO (SI HAY COLUMNAS NUMÉRICAS)
# ==============================

st.subheader("Visualización de datos")

columnas_numericas = df_filtrado.select_dtypes(include=['int64', 'float64']).columns

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