# ─────────────── app.py ───────────────
import streamlit as st
import pandas as pd
import subprocess, time
from pathlib import Path

# Archivos y bridge
INPUT_CSV  = "sentiment_input.csv"
OUTPUT_CSV = "sentiment_output.csv"
BRIDGE_BAT = "knime_bridge.bat"
TIMEOUT    = 1500

st.set_page_config(page_title="Clasificador de Sentimientos",
                   page_icon="💬", layout="centered")

st.title("💬 Clasificador de Sentimientos (KNIME + Streamlit)")
st.write(
    "Escribe una reseña y pulsa **Predecir**. "
    "La reseña se envía a KNIME, que ejecuta el modelo y devuelve "
    "si el sentimiento es **positivo** o **negativo**."
)

texto = st.text_area("✏️ Tu reseña:", height=200)

if st.button("🔍 Predecir", disabled=not texto.strip()):
    # Guardar la reseña
    pd.DataFrame({"reviewText": [texto.strip()]}).to_csv(
        INPUT_CSV, index=False, encoding="utf-8"
    )
    st.info("Reseña guardada. Ejecutando KNIME…")

    # Ejecutar KNIME via bridge
    cmd = [str(Path(BRIDGE_BAT).resolve())]
    try:
        subprocess.run(cmd, check=True, timeout=TIMEOUT, shell=True)
    except subprocess.TimeoutExpired:
        st.error(f"⏰ KNIME tardó más de {TIMEOUT}s.")
        st.stop()
    except subprocess.CalledProcessError as e:
        st.error("❌ KNIME devolvió error:\n\n" + str(e))
        st.stop()

    # Leer el resultado generado
    try:
        resultado = pd.read_csv(OUTPUT_CSV, encoding="utf-8")
    except Exception as e:
        st.error("❌ No se pudo leer la salida:\n\n" + str(e))
        st.stop()

    pred = resultado["Prediction (Sentiment)"].iloc[0].strip().lower()
    emoji = "😊" if pred == "positive" else "☹️"
    st.success(f"{emoji} **Sentimiento:** {pred.capitalize()}")

    with st.expander("📄 Ver CSV completo"):
        st.dataframe(resultado, use_container_width=True)
# ───────────── fin app.py ─────────────
