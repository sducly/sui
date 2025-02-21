import whisperx
import torch
import base64
import os
import tempfile
from TTS.api import TTS
from phonemizer import phonemize
import re
from phonemizer.separator import Separator

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

async def speak(text):
    """
    Génère un fichier audio à partir d'un texte et extrait les phonèmes avec WhisperX.
    """

    # Création d'un fichier audio temporaire
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        tts.tts_to_file(text=text, file_path=temp_audio.name, language="fr", speaker_wav='./voices/femme/femme.wav')
        temp_audio_path = temp_audio.name

    # Détection des phonèmes avec WhisperX
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisperx.load_model("small", device, language="fr")

    # Transcription et alignement phonémique
    audio = whisperx.load_audio(temp_audio_path)
    result = model.transcribe(audio, language="fr")

    # Chargement du modèle d'alignement pour obtenir les phonèmes précis
    align_model, metadata = whisperx.load_align_model(language_code="fr", device=device)
    aligned_result = whisperx.align(result["segments"], align_model, metadata, audio, device)

    visemes_with_times = []

    for segment in aligned_result["segments"]:
        print(f"Segment: {segment}")  # Vérification des données du segment

        if "words" in segment:
            for word_data in segment["words"]:
                if "word" in word_data and "start" in word_data and "end" in word_data:
                    word = word_data["word"]
                    start = word_data["start"]
                    end = word_data["end"]

                    # Utilisation de phonemizer pour obtenir les phonèmes
                    separator = Separator(phone=' ', word=None)
                    phonemes = phonemize(word, language='mb-fr2',separator=separator,backend='espeak-mbrola', strip=True).split(" ")
                    if phonemes:
                        word_duration = end - start
                        phoneme_duration = word_duration / len(phonemes)

                        current_time = start

                        for phoneme in phonemes:
                            visemes_with_times.append({
                                "phoneme": phoneme,
                                "start": current_time,
                                "end": current_time + phoneme_duration
                            })
                            current_time += phoneme_duration  
                    else:
                        print(f"Aucun phonème détecté pour le mot : {word}")
                else:
                    print("Données de mot incomplètes.")


    # Convertir l'audio en base64
    with open(temp_audio_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode('utf-8')

    # Nettoyer le fichier temporaire
    os.remove(temp_audio_path)

    return {
        "phonemes": {"mouthCues": visemes_with_times},
        "audio": audio_data
    }
