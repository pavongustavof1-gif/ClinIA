import streamlit as st
st.title("ClinIA Asistente de Notas en Español 🇲🇽")

audio_value = st.audio_input("Haz clic en el micrófono para empezar a hablar.")
if audio_value:
    st.audio(audio_value)
