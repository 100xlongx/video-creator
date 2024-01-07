from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from bing_image_downloader import downloader
from dotenv import load_dotenv
from openai_wrapper import OpenAIWrapper
import os

load_dotenv()

# Function to get the first image path from the download directory
def get_image_path(topic, output_dir):
    directory = f"{output_dir}/{topic.replace(' ', ' ')}"  # Adjusted for spaces in topic
    files = os.listdir(directory)
    if files:
        # Assuming the first image is the one we want, adjust as needed
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Checking for common image types
                return os.path.join(directory, file)
    return None  # or handle this case as needed

api_key = os.getenv("OPENAI_API_KEY")

openai_wrapper = OpenAIWrapper(api_key)

output_dir = 'assets'
# Define paths and text
background_image_path = 'assets/tiktok_background.jpg'

# Define the size of your background
background_width, background_height = 1080, 1920
image_height = 600

# Calculate the y-coordinate for centering the image vertically
y_coordinate = (background_height - image_height) // 2

top_topic = input("Enter the top text: ")
bottom_topic = input("Enter the bottom text: ")

voice_text = f"Would you rather have{top_topic} or {bottom_topic}?"

# audio_filepath = openai_wrapper.generate_speech(voice_text, file_path=f"audio/{top_topic}-{bottom_topic}.mp3")
# transcription = openai_wrapper.generate_transcription(file_path=audio_filepath, response_format="json")
audio_filepath = f"audio/apple-banana.mp3"
transcription = {"text": "I would rather have an apple than a banana."}

# Load the background image as a clip
background_clip = ImageClip(background_image_path).set_duration(10)  # duration in seconds

top_image = downloader.download(top_topic, limit=1, output_dir=output_dir, force_replace=False, timeout=60, verbose=True)
bottom_image = downloader.download(bottom_topic, limit=1, output_dir=output_dir, force_replace=False, timeout=60, verbose=True)

# Construct the paths to the downloaded images
top_image_path = get_image_path(top_topic, output_dir)
bottom_image_path = get_image_path(bottom_topic, output_dir)

# Load the downloaded images as clips
top_image_clip = ImageClip(top_image_path).set_duration(10).resize(height=image_height)  # You might need to adjust size
bottom_image_clip = ImageClip(bottom_image_path).set_duration(10).resize(height=image_height)  # Adjust size as needed

# Position the image clips
top_image_clip = top_image_clip.set_position(("center", y_coordinate - (image_height * 0.75)))
bottom_image_clip = bottom_image_clip.set_position(("center", y_coordinate + (image_height * 0.75)))

# Create a TextClip object for top text
txt_clip_top = TextClip(top_topic, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_duration(10).set_position(("center", 50))
txt_clip_bottom = TextClip(bottom_topic, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_duration(10).set_position(("center", 1750))
txt_clip_center = TextClip(transcription['text'], fontsize=50, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_position(("center", "center")).set_duration(10);

# Overlay all clips on the first clip
final_clip = CompositeVideoClip([background_clip, top_image_clip, bottom_image_clip, txt_clip_top, txt_clip_bottom, txt_clip_center])

# Write the result to a file
final_clip.write_videofile(f'output/{top_topic}-{bottom_topic}.mp4', fps=24)