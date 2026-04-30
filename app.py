import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# ==========================
# 🏛️ CONFIGURACIÓN UI
# ==========================
st.set_page_config(
    page_title="ONPE - Sistema Electoral",
    page_icon="🗳️",
    layout="wide"
)

st.title("🗳 ONPE - Sistema de Resultados Electorales 2021")
st.subheader("📊 Segunda Vuelta Electoral - Dashboard Interactivo")

st.markdown("""
Sistema de visualización y análisis electoral desarrollado con Machine Learning  
para la transparencia de resultados ciudadanos.
""")

# ==========================
# 📥 CARGA DE DATOS
# ==========================
url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
df = pd.read_csv(url, sep=";", encoding="latin1")

# Limpieza
columnas = ["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]
for col in columnas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["GANADOR"] = df.apply(
    lambda x: "Perú Libre" if x["VOTOS_P1"] > x["VOTOS_P2"] else "Fuerza Popular",
    axis=1
)

# ==========================
# 🔎 SIDEBAR - FILTROS
# ==========================
st.sidebar.header("🔎 Filtros de análisis")

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

# ==========================
# 🔧 FILTRADO DE DATOS
# ==========================
df_filtrado = df.copy()

if candidato != "Todos":
    df_filtrado = df_filtrado[df_filtrado["GANADOR"] == candidato]

if region != "Todos" and "DEPARTAMENTO" in df.columns:
    df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"] == region]

# ==========================
# 📊 KPIs PRINCIPALES
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
# 📈 GRÁFICO PRINCIPAL
# ==========================
st.subheader("📊 Distribución de Votos")

labels = ["Perú Libre", "Fuerza Popular", "Blancos", "Nulos"]
values = [votos_p1, votos_p2, votos_vb, votos_vn]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_title("Resultados Electorales ONPE")
ax.set_ylabel("Votos")

st.pyplot(fig)

# ==========================
# 🤖 MACHINE LEARNING
# ==========================
st.subheader("🤖 Modelo Predictivo Electoral")

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
st.subheader("🧠 Interpretación de resultados")

st.markdown(f"""
- El sistema analiza resultados electorales por región y candidato.
- El modelo de Machine Learning alcanza una precisión de **{acc:.2f}**.
- Se identifican patrones de votación en mesas electorales.
- Los votos blancos y nulos son considerados en el análisis.

✔ Este sistema permite transparencia y análisis ciudadano de datos electorales.
""")

# ==========================
# 🔄 USER FLOW
# ==========================
st.subheader("🔄 Flujo del Usuario (User Flow)")

st.markdown("""
**1️⃣ Selección de filtros**
- El usuario selecciona región o candidato desde el panel lateral.

**2️⃣ Visualización de resultados**
- Se muestran gráficos, KPIs y distribución de votos.

**3️⃣ Interpretación**
- El sistema presenta un análisis automático de resultados y precisión del modelo.

➡️ Esto permite una experiencia clara, intuitiva y orientada a la ciudadanía.
""")

# ==========================
# 📌 DATA PREVIEW
# ==========================
with st.expander("📂 Ver datos utilizados"):
    st.dataframe(df_filtrado.head())
