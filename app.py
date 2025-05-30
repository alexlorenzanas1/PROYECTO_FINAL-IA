import streamlit as st
import time

st.set_page_config(page_title="Clasificador Demo", page_icon="💬", layout="centered")

st.title("💬 Clasificador de Sentimientos (Demo)")
st.write(
    "Escribe una reseña y pulsa **Predecir**. Esta es una demo, la predicción es automática (positiva)."
)

# Área de entrada
texto = st.text_area("✏️ Tu reseña:", height=200)

# Botón
if st.button("🔍 Predecir", disabled=not texto.strip()):
    with st.spinner("Analizando reseña..."):
        time.sleep(2)  # Simula procesamiento
    st.success("😊 **Sentimiento:** Positive")

    st.toast("✔️ Reseña procesada correctamente", icon="✅")
