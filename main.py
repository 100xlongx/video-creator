from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioClip, AudioFileClip
from dotenv import load_dotenv
from openai_wrapper import OpenAIWrapper
from helpers import create_image_path_from_keyword
import os

load_dotenv()

openai_wrapper = OpenAIWrapper(os.getenv("OPENAI_API_KEY"))

# Define the size of your background
background_width, background_height = 1080, 1920
image_height = 600

# Calculate the y-coordinate for centering the image vertically
y_coordinate = (background_height - image_height) // 2

top_topic = input("Enter the top text: ")
bottom_topic = input("Enter the bottom text: ")

voice_text = f"Would you rather pick {top_topic} or {bottom_topic}?"

audio_filepath = openai_wrapper.generate_speech(voice_text, file_path=f"audio/{top_topic}-{bottom_topic}.mp3")
# transcription = openai_wrapper.generate_transcription(file_path=audio_filepath, response_format="json")
# audio_filepath = f"audio/apple-banana.mp3"

top_start_time = 1
bottom_start_time = top_start_time + 2

# Load the background image as a clip
background_clip = ImageClip('assets/tiktok_background.jpg').set_duration(10)  # duration in seconds

# Construct the paths to the downloaded images
top_image_path = create_image_path_from_keyword(top_topic)
bottom_image_path = create_image_path_from_keyword(bottom_topic)

# Create image clips for the top and bottom images
top_image_clip = ImageClip(top_image_path).set_duration(10).resize(height=image_height).set_position(("center", y_coordinate - (image_height * 0.75))).crossfadein(1).set_start(top_start_time)
bottom_image_clip = ImageClip(bottom_image_path).set_duration(10).resize(height=image_height).set_position(("center", y_coordinate + (image_height * 0.75))).crossfadein(1).set_start(bottom_start_time)

# Create text clips for bottom, top and middle text
txt_clip_top = TextClip(top_topic, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_duration(10).set_position(("center", 50)).set_start(top_start_time)
txt_clip_bottom = TextClip(bottom_topic, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana', method='caption', align='center').set_duration(10).set_position(("center", 1750)).set_start(bottom_start_time)
# txt_clip_center = TextClip(transcription['text'], fontsize=50, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_position(("center", "center")).set_duration(10);

# add audios
audio_clip = AudioFileClip(audio_filepath)

# Overlay all clips on the first clip
final_clip = CompositeVideoClip([background_clip, top_image_clip, bottom_image_clip, txt_clip_top, txt_clip_bottom]).set_audio(audio_clip)

# Write the result to a file
final_clip.write_videofile(f'output/{top_topic}-{bottom_topic}.mp4', fps=24)