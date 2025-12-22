import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title("ClinIA Asistente de Notas en Español 🇲🇽")
st.write("Haz clic en el micrófono para empezar a hablar.")

# 1. The Recording Component
audio = mic_recorder(
    start_prompt="🔴 Iniciar Grabación",
    stop_prompt="⏹️ Detener y Procesar",
    key='recorder'
)

# 2. Logic to handle the recorded audio
if audio:
    st.audio(audio['bytes']) # Playback for the user to confirm
    st.success("Grabación capturada exitosamente.")
    
    # This is where we hand off to the next building block:
    # process_with_ai(audio['bytes']) 

