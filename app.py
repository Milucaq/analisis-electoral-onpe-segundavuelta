import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# =========================
# TÍTULO INSTITUCIONAL
# =========================
st.title("🗳 ONPE - Sistema de Resultados Electorales 2021")
st.subheader("📊 Visualización y análisis de segunda vuelta")

# =========================
# CARGA DE DATOS
# =========================
url = "https://raw.githubusercontent.com/Milucaq/analisis-electoral-onpe-segundavuelta/main/Resultados_2da_vuelta_Version_PCM.csv"
df = pd.read_csv(url, sep=";", encoding="latin1")

columnas = ["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]
for col in columnas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["GANADOR"] = df.apply(lambda x: "Perú Libre" if x["VOTOS_P1"] > x["VOTOS_P2"] else "Fuerza Popular", axis=1)

# =========================
# FILTROS
# =========================
st.sidebar.header("🔎 Filtros de búsqueda")

candidato = st.sidebar.selectbox(
    "Selecciona candidato",
    ["Todos", "Perú Libre", "Fuerza Popular"]
)

# Región si existe en dataset (ajustable)
if "DEPARTAMENTO" in df.columns:
    region = st.sidebar.selectbox("Selecciona región", ["Todos"] + list(df["DEPARTAMENTO"].unique()))
else:
    region = "Todos"

# =========================
# APLICAR FILTROS
# =========================
df_filtrado = df.copy()

if candidato != "Todos":
    df_filtrado = df_filtrado[df_filtrado["GANADOR"] == candidato]

if region != "Todos" and "DEPARTAMENTO" in df.columns:
    df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"] == region]

# =========================
# VISUALIZACIÓN
# =========================
st.subheader("📊 Resultados Electorales")

votos_p1 = df_filtrado["VOTOS_P1"].sum()
votos_p2 = df_filtrado["VOTOS_P2"].sum()
votos_vb = df_filtrado["VOTOS_VB"].sum()
votos_vn = df_filtrado["VOTOS_VN"].sum()

labels = ["Perú Libre", "Fuerza Popular", "Blancos", "Nulos"]
values = [votos_p1, votos_p2, votos_vb, votos_vn]

fig, ax = plt.subplots()
ax.bar(labels, values)
st.pyplot(fig)

# =========================
# INTERPRETACIÓN
# =========================
st.subheader("🧠 Interpretación")

st.write(f"""
- El candidato con mayor votación en el filtro seleccionado es analizado automáticamente.
- Se observa la distribución de votos válidos, blancos y nulos.
- Este sistema permite transparencia y comprensión de resultados electorales.
""")

# =========================
# MACHINE LEARNING (opcional visual)
# =========================
st.subheader("🤖 Modelo predictivo")

df_ml = df.copy()
df_ml["GANADOR_NUM"] = df_ml.apply(lambda x: 1 if x["VOTOS_P1"] > x["VOTOS_P2"] else 0, axis=1)

X = df_ml[["VOTOS_P1", "VOTOS_P2", "VOTOS_VB", "VOTOS_VN"]]
y = df_ml["GANADOR_NUM"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = DecisionTreeClassifier(max_depth=5)
modelo.fit(X_train, y_train)

acc = accuracy_score(y_test, modelo.predict(X_test))

st.write("Precisión del modelo:", round(acc, 2))
