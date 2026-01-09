# —————————— Declarations ————————-

import streamlit as st
import assemblyai as aai

#adapted from AssemblyAI
import asyncio
from typing import Dict, List
from assemblyai.types import (
    SpeakerOptions,
    PIIRedactionPolicy,
    PIISubstitutionPolicy,
)

aai.settings.api_key = "077c7fb352f4406b8d99cc78f999cb3a"    # <— move to secrets

#Adapted from AssemblyAI

async def transcribe_encounter_async(audio_source: str) -> Dict:
  
#    Asynchronously transcribe a medical encounter with Slam-1
#    Args:
#        audio_source: Either a local file path or publicly accessible URL
 
    # Configure comprehensive medical transcription
    config = aai.TranscriptionConfig(
        speech_model=aai.SpeechModel.universal,
        # Diarize provider and patient
        language_code="es",
        speaker_labels=True,
        speakers_expected=2,  # Typically provider and patient
        # Punctuation and Formatting
        punctuate=True,
        format_text=True,

        # Boost accuracy of medical terminology
        keyterms_prompt=[
            # Patient-specific context
            "hypertensión", "diabetes mellitus tipo 2", "metformina",

            # Specialty-specific terms
            "auscultación", "palpación", "diagnóstico diferenciado",
            "queja principal", "revisión de los sistemas", "exámen físico",

            # Common medications
            "lisinopril", "atorvastatina", "levotiroxina",

            # Procedure terms
            "electrocardiograma", "conteo de sangre", "hemoglobina A1c"
        ],

        # Speech understanding for medical documentation
        entity_detection=True,  # Extract medications, conditions, procedures
    #    redact_pii=True,  # HIPAA compliance
    #    redact_pii_policies=[
    #        PIIRedactionPolicy.person_name,
    #        PIIRedactionPolicy.date_of_birth,
    #        PIIRedactionPolicy.phone_number,
    #        PIIRedactionPolicy.email_address,
    #    ],
   #     redact_pii_sub=PIISubstitutionPolicy.hash,
   #     redact_pii_audio=True  # Create HIPAA-compliant audio
    )
# ^^^Aquí

# config = aai.TranscriptionConfig(
#    format_text=True,
#    punctuate=True,
#    language_code="es",
#    speaker_labels=True
# )
# config.speech_models = [
#    "universal"
# ]


# —————————- Page Headers ————————

st.set_page_config(page_title="Note Taker Alpha")

st.title("Asistente de Notas en Español 🇲🇽")
st.info("Alpha v0.1 - Grabación Directa")

# ————————- Functions ——————————-

# ———————— Transcription phase —————-

def transcription_phase(audio_source):
    # Phase A: Converts audio (local file or URL) into a Transcript object.
#    config = aai.TranscriptionConfig(
#        format_text=True,
#        punctuate=True,
#        language_code="es",
#        speaker_labels=True
#    )
#    config.speech_models = [
#        "universal"
#    ]

    # Initialize the Transcriber
    transcriber = aai.Transcriber(config = config)

    st.write("Starting transcription for: {audio_source}") 
    
    # This call is synchronous and will block until the transcript is ready
    transcript = transcriber.transcribe(audio_source) 

    # Error handling
    if transcript.status == aai.TranscriptStatus.error:
        st.write(f"Transcription failed: {transcript.error}")
        return None

    st.write("Transcription successful!")
    return transcript







# ———————— Main body —————————-

audio_data = st.audio_input("Haz clic en el micrófono para grabar la conversación")

if audio_data:
    # 1. Show the player so the user can verify the audio
    st.audio(audio_data)
    st.success("Audio capturado. Listo para procesar.")
    
    # 2. Convert to bytes for our AI services
    filename = "recorded_audio.wav"
    with open(filename, "wb") as f:
        f.write(audio_data.getvalue())

    st.write(f"Saved to {filename}")
    # Now you can use `filename` or `audio_value.getvalue()` in your API call

    result = transcription_phase(filename)
    if result:
        st.write ("Tu dijiste:  ",result.text)
    
        if st.button("Generar Resumen y Google Doc"):
            with st.spinner("Transcribiendo y analizando..."):
                # This is where we will plug in the Transcription + LLM logic
                st.write("Siguiente paso: Enviando a la IA...")

