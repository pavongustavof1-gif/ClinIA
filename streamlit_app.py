import streamlit as st
st.title("ClinIA Asistente de Notas en Español 🇲🇽")
st.write("Haz clic en el micrófono para empezar a hablar.")


audio_value = st.audio_input("Record a voice message")
if audio_value:
    st.audio(audio_value)
    st.success("Grabación capturada exitosamente.")

