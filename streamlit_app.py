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
# —————————- Page Headers ————————

st.set_page_config(page_title="Note Taker Alpha")

st.title("Asistente de Notas en Español 🇲🇽")
st.info("Alpha v0.1 - Grabación Directa")


aai.settings.api_key = "077c7fb352f4406b8d99cc78f999cb3a"    # <— move to secrets

# ————————- Functions ——————————-
#Adapted from AssemblyAI

def transcribe_encounter (audio_source): # : str) -> Dict:
  
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





# ———————— Transcription phase —————-

# def transcription_phase(audio_source):

    # Initialize the Transcriber
transcriber = aai.Transcriber()  # (config=config)   <-- OJO

st.write("Starting transcription for: {audio_source}") 
    
    # This call is synchronous and will block until the transcript is ready
transcript = transcriber.transcribe(audio_source, config = config) 

    # Error handling
    if transcript.status == aai.TranscriptStatus.error:
        st.write("Transcription failed: {transcript.error}")
        return None

    st.write("Transcription successful!")
    sr.write("Diálogo entre paciente y médico")
    for utterance in transcript.utterances:
            # Format timestamp
            start_time = utterance.start / 1000  # Convert to seconds
            end_time = utterance.end / 1000

            # Identify speaker role
            speaker_label = "Médico" if utterance.speaker == "A" else "Paciente"

            # Print formatted utterance
     #       st.write([{start_time:.1f}s - {end_time:.1f}s] {speaker_label}:")
            st.write(" {speaker_label}:")
            st.write("  {utterance.text}")
    #        st.write("  Confidence: {utterance.confidence:.2%}\n")

        # Extract clinical entities
        if transcript.entities:
            print("\n=== Entidades Clínicas Detectadas ===\n")
            medications = [e for e in transcript.entities if e.entity_type == "medication"]
            conditions = [e for e in transcript.entities if e.entity_type == "medical_condition"]
            procedures = [e for e in transcript.entities if e.entity_type == "medical_procedure"]

            if medications:
                st.write("Medicamento:", ", ".join([m.text for m in medications]))
            if conditions:
                st.write("Condiciónes:", ", ".join([c.text for c in conditions]))
            if procedures:
                sr.write("Procedimientos:", ", ".join([p.text for p in procedures]))
                
        return {
            "transcript": transcript,
            "utterances": transcript.utterances,
            "entities": transcript.entities,
            "redacted_audio_url": transcript.redacted_audio_url
        }

    except Exception as e:
        st.write("Error during transcription: {e}")
        raise




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

    try:
        result = await transcribe_encounter(filename)

        # Additional processing
        st.write("\nEncounter duration: {result['transcript'].audio_duration} seconds")

        # Could send to LLM Gateway for SOAP note generation here

    except Exception as e:
        print(f"Failed to process encounter: {e}")


#   result = transcribe_encounter (filename) # transcription_phase(filename)
#    if result:
#        st.write ("Tu dijiste:  ",result.text)
    
 #       if st.button("Generar Resumen y Google Doc"):
 #           with st.spinner("Transcribiendo y analizando..."):
 #               # This is where we will plug in the Transcription + LLM logic
 #               st.write("Siguiente paso: Enviando a la IA...")

