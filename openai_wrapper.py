from openai import OpenAI
from helpers import generate_hash, check_if_voice_over_exists

class OpenAIWrapper:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_speech(self, text: str, model="tts-1", voice="onyx", output_dir="audio/voice_overs/"):\
        #create a hash of the text to use as the file name
        file_hash = generate_hash(text)
        file_path = f"{output_dir}{file_hash}.mp3"

        if not check_if_voice_over_exists(file_hash, output_dir=output_dir):
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            response.stream_to_file(file_path)
        
        return file_path
    
    def generate_transcription(self, file_path="audio/voice_overs/speech.mp3", model="whisper-1", response_format="json"):
        response = self.client.audio.transcriptions.create(
            model=model,
            file=open(file_path, "rb"),
            response_format=response_format
        )

        return response