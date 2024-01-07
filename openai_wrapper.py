from openai import OpenAI

class OpenAIWrapper:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_speech(self, text, model="tts-1", voice="onyx", file_path="audio/speech.mp3"):
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(file_path)
        return file_path
    
    def generate_transcription(self, file_path="audio/speech.mp3", model="whisper-1", response_format="json"):
        response = self.client.audio.transcriptions.create(
            model=model,
            file=open(file_path, "rb"),
            response_format=response_format
        )

        return response