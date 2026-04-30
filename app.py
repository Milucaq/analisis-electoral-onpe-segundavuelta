import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Resultados ONPE", layout="wide")

# Título
st.title("Resultados Electorales ONPE 2021")

# ==============================
# CARGAR DATOS (DESDE EL REPO)
# ==============================

@st.cache_data
def cargar_datos():
    return pd.read_csv("Resultados_2da_vuelta_Version_PCM.csv", encoding='latin1')

df = cargar_datos()

# ==============================
# VISTA GENERAL
# ==============================

st.subheader("Vista general del dataset")
st.dataframe(df.head())

# ==============================
# FILTRO POR DEPARTAMENTO
# ==============================

# Ajuste automático (primera columna)
columna_departamento = df.columns[0]

departamentos = df[columna_departamento].dropna().unique()

depto_seleccionado = st.selectbox(
    "Selecciona un departamento:",
    departamentos
)

df_filtrado = df[df[columna_departamento] == depto_seleccionado]

# ==============================
# MOSTRAR DATOS
# ==============================

st.subheader(f"Datos del departamento: {depto_seleccionado}")
st.dataframe(df_filtrado)

# ==============================
# GRÁFICO
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
