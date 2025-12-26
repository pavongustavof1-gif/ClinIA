st.set_page_config(page_title="Note Taker Alpha", page_icon="📝")

st.title("ClinIA Asistente de Notas en Español 🇲🇽")
st.info("Alpha v0.1 - Grabación Directa")
 
# The NEW native Streamlit component (Available in Streamlit 1.40+)
audio_data = st.audio_input("Haz clic en el micrófono para grabar la conversación")
 
if audio_data:
    # 1. Show the player so the user can verify the audio
    st.audio(audio_data)
    st.success("Audio capturado. Listo para procesar.")
    
    # 2. Convert to bytes for our AI services
    # raw_audio_bytes = audio_data.read()
    
    if st.button("Generar Resumen y Google Doc"):
        with st.spinner("Transcribiendo y analizando..."):
            # This is where we will plug in the Transcription + LLM logic
            st.write("Siguiente paso: Enviando a la IA...")
