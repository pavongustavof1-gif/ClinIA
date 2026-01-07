import streamlit as st
import assemblyai as aai

st.set_page_config(page_title="Note Taker Alpha")

st.title("Asistente de Notas en Español 🇲🇽")
st.info("Alpha v0.1 - Grabación Directa")

# The NEW native Streamlit component (Available in Streamlit 1.40+)
audio_data = st.audio_input("Haz clic en el micrófono para grabar la conversación")

if audio_data:
    # 1. Show the player so the user can verify the audio
    st.write ("recibido en if audio_data")
    st.audio(audio_data)
    st.success("Audio capturado. Listo para procesar.")
    
    # 2. Convert to bytes for our AI services
    raw_audio_bytes = audio_data.read()

    
    if st.button("Generar Resumen y Google Doc"):
        with st.spinner("Transcribiendo y analizando..."):
            # This is where we will plug in the Transcription + LLM logic
            st.write("Siguiente paso: Enviando a la IA...")

# 1. Setup your API Key
aai.settings.api_key = "077c7fb352f4406b8d99cc78f999cb3a"
def transcription_phase(audio_source):
    st.write ("transcription_phase llamado") # <-- 
  
    # Phase A: Converts audio (local file or URL) into a Transcript object.

    # Initialize the Transcriber
    transcriber = aai.Transcriber()

    print(f"Starting transcription for: {audio_source}") # audio_data??
    
    # This call is synchronous and will block until the transcript is ready
    transcript = transcriber.transcribe(audio_source)  # audio_data??

    # Error handling
    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
        return None

    print("Transcription successful!")
    return transcript

# Example Usage:
st.write ("listo para enviar a transcription phase")  # <--
result = transcription_phase(raw_audio_bytes)
if result:
    print(result.text)

# config = aai.TranscriptionConfig(speaker_labels=True, auto_chapters=True)
# transcript = transcriber.transcribe(audio_source, config=config)
