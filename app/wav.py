import asyncio
import edge_tts
import time
import base64

async def generate_audio(text):
    voice = "fr-FR-DeniseNeural"  # Voix française féminine
    output_file = "output.mp3"
    communicator = edge_tts.Communicate(text, voice)
    start = time.perf_counter()
    await communicator.save(output_file)
    end = time.perf_counter()
    print(f"Audio généré en {end - start:.3f} sec")
    
    # Encodage en base64
    with open(output_file, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode("utf-8")
    return audio_data

async def main():
    text = ("Bonjour, Sui va bien et toi ? "
            "Si tu as besoin d'aide, n'hésite pas à demander à Sui. "
            "Sinon, casse-toi !")
    audio_data = await generate_audio(text)
    print("Longueur de l'audio encodé (base64):", len(audio_data))

if __name__ == "__main__":
    asyncio.run(main())
