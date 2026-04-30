import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# ==========================
# 🏛 CONFIGURACIÓN
# ==========================
st.set_page_config(page_title="ONPE Sistema Electoral", page_icon="🗳️", layout="wide")

st.title("🗳 ONPE - Sistema de Análisis Electoral")
st.subheader("📊 Segunda Vuelta - Visualización y Machine Learning")

# ==========================
# 📥 DATASET
# ==========================
url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
df = pd.read_csv(url, sep=";", encoding="latin1")

columnas = ["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]
for col in columnas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["GANADOR"] = df.apply(lambda x: "Perú Libre" if x["VOTOS_P1"] > x["VOTOS_P2"] else "Fuerza Popular", axis=1)

# ==========================
# 🔎 CONSULTA POR MESA
# ==========================
st.sidebar.header("🔎 Consulta Electoral")

if "MESA_DE_VOTACION" in df.columns:
    mesa = st.sidebar.selectbox("Selecciona mesa de votación", df["MESA_DE_VOTACION"].unique())
    df = df[df["MESA_DE_VOTACION"] == mesa]

candidato = st.sidebar.selectbox("Candidato", ["Todos", "Perú Libre", "Fuerza Popular"])

if candidato != "Todos":
    df = df[df["GANADOR"] == candidato]

# ==========================
# 📊 KPIs
# ==========================
votos_p1 = df["VOTOS_P1"].sum()
votos_p2 = df["VOTOS_P2"].sum()
votos_vb = df["VOTOS_VB"].sum()
votos_vn = df["VOTOS_VN"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Perú Libre", int(votos_p1))
col2.metric("Fuerza Popular", int(votos_p2))
col3.metric("Blancos", int(votos_vb))
col4.metric("Nulos", int(votos_vn))

# ==========================
# 📉 GRÁFICO BARRAS (PEQUEÑO)
# ==========================
st.subheader("📉 Comparación de Votos")

labels = ["Perú Libre", "Fuerza Popular", "Blancos", "Nulos"]
values = [votos_p1, votos_p2, votos_vb, votos_vn]

fig1, ax1 = plt.subplots(figsize=(4, 3))
ax1.bar(labels, values)
ax1.set_title("Votos por categoría")
st.pyplot(fig1)

# ==========================
# 🥧 GRÁFICO CIRCULAR
# ==========================
st.subheader("🥧 Distribución porcentual")

fig2, ax2 = plt.subplots()
ax2.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
ax2.set_title("Distribución Electoral")
st.pyplot(fig2)

# ==========================
# 🤖 MACHINE LEARNING
# ==========================
st.subheader("🤖 Análisis Predictivo")

df_ml = df.copy()
df_ml["GANADOR_NUM"] = df_ml.apply(lambda x: 1 if x["VOTOS_P1"] > x["VOTOS_P2"] else 0, axis=1)

X = df_ml[["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]]
y = df_ml["GANADOR_NUM"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = DecisionTreeClassifier(max_depth=5)
modelo.fit(X_train, y_train)

acc = accuracy_score(y_test, modelo.predict(X_test))

st.metric("🎯 Precisión del modelo", f"{acc:.2f}")

# ==========================
# 🧠 INTERPRETACIÓN
# ==========================
st.subheader("🧠 Interpretación")

st.markdown(f"""
- Se analizan votos por mesa de votación.
- Se permite filtrado por candidato.
- El modelo de Machine Learning obtiene una precisión de **{acc:.2f}**.
- Se visualizan datos en gráficos de barras y circular.

✔ Sistema orientado a transparencia electoral y análisis ciudadano.
""")

# ==========================
# 📂 DATOS
# ==========================
with st.expander("📂 Ver datos"):
    st.dataframe(df.head())
