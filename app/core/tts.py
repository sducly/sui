import whisperx
import torch
import base64
import os
import tempfile
import edge_tts
from phonemizer import phonemize
from phonemizer.separator import Separator
from concurrent.futures import ProcessPoolExecutor

# --- Initialisation des modèles WhisperX ---
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisperx.load_model("small", device, language="fr")
align_model, metadata = whisperx.load_align_model(language_code="fr", device=device)

def process_word(word_data):
    """
    Traite un mot : calcule ses phonèmes et renvoie les visèmes avec leurs timings.
    Cette fonction sera appelée en parallèle.
    """
    separator = Separator(phone=' ', word=None)
    if "word" in word_data and "start" in word_data and "end" in word_data:
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]
        phonemes = phonemize(word, language='mb-fr2', separator=separator, backend='espeak-mbrola', strip=True).split(" ")
        visemes = []
        if phonemes:
            word_duration = end - start
            phoneme_duration = word_duration / len(phonemes)
            current_time = start
            for phoneme in phonemes:
                visemes.append({
                    "phoneme": phoneme,
                    "start": current_time,
                    "end": current_time + phoneme_duration
                })
                current_time += phoneme_duration
        return visemes
    return []

async def speak(text):

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio_path = temp_audio.name

    voice = "fr-FR-DeniseNeural"
    communicator = edge_tts.Communicate(text, voice)
    await communicator.save(temp_audio_path)

    
    audio = whisperx.load_audio(temp_audio_path)
    result = model.transcribe(audio, language="fr")

    aligned_result = whisperx.align(result["segments"], align_model, metadata, audio, device)

    words = []
    for segment in aligned_result["segments"]:
        if "words" in segment:
            words.extend(segment["words"])
    
    visemes_with_times = []
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_word, words))
    for res in results:
        visemes_with_times.extend(res)

    with open(temp_audio_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode('utf-8')

    os.remove(temp_audio_path)

    return {
        "phonemes": {"mouthCues": visemes_with_times},
        "audio": audio_data
    }