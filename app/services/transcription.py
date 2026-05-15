from openai import OpenAI

from app.settings import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY, base_url='https://api.groq.com/openai/v1'
)


def transcribe_audio(file_path: str) -> str:
    with open(file_path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model='whisper-large-v3',
        )

    return transcription.text
