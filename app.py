import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# ==========================
# 🏛 CONFIGURACIÓN
# ==========================
st.set_page_config(
    page_title="ONPE - Sistema Electoral",
    page_icon="🗳️",
    layout="wide"
)

st.title("🗳 ONPE - Sistema de Resultados Electorales 2021")
st.subheader("📊 Dashboard Interactivo de Segunda Vuelta")

st.markdown("""
Sistema de análisis electoral con Machine Learning y visualización de resultados.
""")

# ==========================
# 📥 CARGA DE DATOS
# ==========================
url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
df = pd.read_csv(url, sep=";", encoding="latin1")

columnas = ["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]
for col in columnas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["GANADOR"] = df.apply(
    lambda x: "Perú Libre" if x["VOTOS_P1"] > x["VOTOS_P2"] else "Fuerza Popular",
    axis=1
)

# ==========================
# 🔎 FILTROS
# ==========================
st.sidebar.header("🔎 Filtros")

candidato = st.sidebar.selectbox(
    "Selecciona candidato",
    ["Todos", "Perú Libre", "Fuerza Popular"]
)

if "DEPARTAMENTO" in df.columns:
    region = st.sidebar.selectbox(
        "Selecciona región",
        ["Todos"] + sorted(df["DEPARTAMENTO"].unique())
    )
else:
    region = "Todos"

df_filtrado = df.copy()

if candidato != "Todos":
    df_filtrado = df_filtrado[df_filtrado["GANADOR"] == candidato]

if region != "Todos" and "DEPARTAMENTO" in df.columns:
    df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"] == region]

# ==========================
# 📊 KPIs
# ==========================
votos_p1 = df_filtrado["VOTOS_P1"].sum()
votos_p2 = df_filtrado["VOTOS_P2"].sum()
votos_vb = df_filtrado["VOTOS_VB"].sum()
votos_vn = df_filtrado["VOTOS_VN"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Perú Libre", int(votos_p1))
col2.metric("Fuerza Popular", int(votos_p2))
col3.metric("Blancos", int(votos_vb))
col4.metric("Nulos", int(votos_vn))

# ==========================
# 📊 GRÁFICO DE BARRAS (PEQUEÑO)
# ==========================
st.subheader("📉 Gráfico de Barras (Comparación)")

fig1, ax1 = plt.subplots(figsize=(4, 3))  # 🔥 más pequeño

labels = ["Perú Libre", "Fuerza Popular", "Blancos", "Nulos"]
values = [votos_p1, votos_p2, votos_vb, votos_vn]

ax1.bar(labels, values)
ax1.set_title("Votos")
ax1.set_ylabel("Cantidad")

st.pyplot(fig1)

# ==========================
# 🥧 GRÁFICO CIRCULAR
# ==========================
st.subheader("🥧 Distribución Porcentual de Votos")

fig2, ax2 = plt.subplots()

ax2.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

ax2.set_title("Distribución Electoral")

st.pyplot(fig2)

# ==========================
# 🤖 MACHINE LEARNING
# ==========================
st.subheader("🤖 Modelo Predictivo")

df_ml = df.copy()
df_ml["GANADOR_NUM"] = df_ml.apply(
    lambda x: 1 if x["VOTOS_P1"] > x["VOTOS_P2"] else 0,
    axis=1
)

X = df_ml[["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]]
y = df_ml["GANADOR_NUM"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

modelo = DecisionTreeClassifier(max_depth=5)
modelo.fit(X_train, y_train)

acc = accuracy_score(y_test, modelo.predict(X_test))

st.metric("🎯 Precisión del modelo", f"{acc:.2f}")

# ==========================
# 🧠 INTERPRETACIÓN
# ==========================
st.subheader("🧠 Interpretación")

st.markdown(f"""
- Se analiza la distribución de votos por candidato.
- El modelo de Machine Learning tiene una precisión de **{acc:.2f}**.
- El gráfico circular permite ver proporciones claras.
- El gráfico de barras compara valores absolutos.

✔ Sistema orientado a transparencia electoral.
""")

# ==========================
# 🔄 USER FLOW
# ==========================
st.subheader("🔄 Flujo del Usuario")

st.markdown("""
**1️⃣ Selección de filtros**
- Región o candidato desde la barra lateral.

**2️⃣ Visualización de datos**
- Gráfico de barras (comparación)
- Gráfico circular (porcentajes)
- KPIs en tarjetas

**3️⃣ Interpretación**
- Análisis automático de resultados
- Precisión del modelo predictivo
""")

# ==========================
# 📂 DATOS
# ==========================
with st.expander("📂 Ver datos"):
    st.dataframe(df_filtrado.head())
