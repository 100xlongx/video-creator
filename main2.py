from openai_wrapper import OpenAIWrapper
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai_wrapper = OpenAIWrapper(api_key)

# speech_file_path = "audio/speech.mp3"
voice_text = "Today is a wonderful day to build something people love!"

# # Use the wrapper to generate speech
# filepath = openai_wrapper.generate_speech(text_to_speech, file_path=speech_file_path)

# transcription = openai_wrapper.generate_transcription()
audio_filepath = openai_wrapper.generate_speech(voice_text, file_path=f"audio/test.mp3")

transcription = openai_wrapper.generate_transcription(file_path=audio_filepath)

textChannel = transcription.text


print(textChannel)