# —————————— Declarations ————————-

import streamlit as st
import assemblyai as aai

aai.settings.api_key = "077c7fb352f4406b8d99cc78f999cb3a"    # <— move to secrets

config = aai.TranscriptionConfig(
    format_text=True,
    punctuate=True,
    language_code="es"    
)
config.speech_models = [
    "universal"
]


# —————————- Page Headers ————————

st.set_page_config(page_title="Note Taker Alpha")

st.title("Asistente de Notas en Español 🇲🇽")
st.info("Alpha v0.1 - Grabación Directa")

# ————————- Functions ——————————-

# ———————— Transcription phase —————-

def transcription_phase(audio_source):
    st.write ("transcription_phase llamado") # <-- debug only
  
    # Phase A: Converts audio (local file or URL) into a Transcript object.

    # Initialize the Transcriber
    transcriber = aai.Transcriber()

    print(f"Starting transcription for: {audio_source}") 
    
    # This call is synchronous and will block until the transcript is ready
    transcript = transcriber.transcribe(audio_source) 

    # Error handling
    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
        return None

    print("Transcription successful!")
    return transcript







# ———————— Main body —————————-

audio_data = st.audio_input("Haz clic en el micrófono para grabar la conversación")

if audio_data:
    # 1. Show the player so the user can verify the audio
    st.write ("recibido en if audio_data") # <—— debug only
    st.audio(audio_data)
    st.success("Audio capturado. Listo para procesar.")
    
    # 2. Convert to bytes for our AI services
    filename = "recorded_audio.wav"
    with open(filename, "wb") as f:
        f.write(audio_data.getvalue())

    st.write(f"Saved to {filename}")
    # Now you can use `filename` or `audio_value.getvalue()` in your API call

    st.write ("listo para enviar a transcription phase")  # <--
    result = transcription_phase(filename)
    if result:
        print(result.text)
    
        if st.button("Generar Resumen y Google Doc"):
            with st.spinner("Transcribiendo y analizando..."):
                # This is where we will plug in the Transcription + LLM logic
                st.write("Siguiente paso: Enviando a la IA...")

# config = aai.TranscriptionConfig(speaker_labels=True, auto_chapters=True)
# transcript = transcriber.transcribe(audio_source, config=config)
