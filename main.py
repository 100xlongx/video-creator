from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip, concatenate_audioclips
from dotenv import load_dotenv
from openai_wrapper import OpenAIWrapper
from helpers import create_image_path_from_keyword
import argparse
import os

load_dotenv()

openai_wrapper = OpenAIWrapper(os.getenv("OPENAI_API_KEY"))
background_width, background_height, image_height = 1080, 1920, 600
y_coordinate = (background_height - image_height) // 2

parser = argparse.ArgumentParser(description="Video Creation Tool")

parser.add_argument("-tt", "--top_text", required=True, help="The top text")
parser.add_argument("-bt", "--bottom_text", required=True, help="Enter the bottom text")

parser.add_argument("-tp", "--top_prompt", help="Enter the top prompt (optional, defaults to top text if not provided)")
parser.add_argument("-bp", "--bottom_prompt", help="Enter the bottom prompt (optional, defaults to bottom text if not provided)")

# parser.add_argument("-vf", "--voiceover_file", required=False, help="Path to the voiceover audio file (will use openAI to create one if not provided)")
parser.add_argument("-o", "--output", required=False, help="Output file path")

parser.add_argument("--image_source", choices=['bing', 'dalle', 'manual'], default='bing', help="Choose the image source: bing (default), dalle, or manual")
parser.add_argument("--top_image_url", help="URL for the top image (required if image_source is manual)")
parser.add_argument("--bottom_image_url", help="URL for the bottom image (required if image_source is manual)")

args = parser.parse_args()

top_text = args.top_text
bottom_text = args.bottom_text

top_prompt = args.top_prompt if args.top_prompt is not None else top_text
bottom_prompt = args.bottom_prompt if args.bottom_prompt is not None else bottom_text

# default output path has underscores instead of spaces
output = args.output if args.output is not None else f"output/red_blue/{top_text.replace(' ', '_')}-{bottom_text.replace(' ', '_')}.mp4"

if args.image_source == 'dalle':
    # Code to call the DALL-E API for images using top_prompt and bottom_prompt
    # You will need to implement the logic for calling DALL-E API
    pass
elif args.image_source == 'manual':
    if not args.top_image_url or not args.bottom_image_url:
        parser.error("Top and bottom image URLs are required when image_source is set to manual.")
    top_image_path = args.top_image_url
    bottom_image_path = args.bottom_image_url
else:  # Default to Bing image downloader
    top_image_path = create_image_path_from_keyword(top_prompt)
    bottom_image_path = create_image_path_from_keyword(bottom_prompt)

voiceover_filepath = openai_wrapper.generate_speech(f"Would you rather pick {top_text} or {bottom_text}?")

# transcription = openai_wrapper.generate_transcription(file_path=audio_filepath, response_format="json")
# voiceover_filepath = f"audio/rick sanchez turning himself into a pickle-travis scott fortnite skin.mp3"

video_duration = 10
top_start_time = 1
bottom_start_time = top_start_time + 2

# Load the background image as a clip
background_clip = ImageClip('assets/tiktok_background.jpg').set_duration(video_duration)  # duration in seconds

# Construct the paths to the downloaded images
top_image_path = create_image_path_from_keyword(top_prompt)
bottom_image_path = create_image_path_from_keyword(bottom_prompt)

# Create image clips for the top and bottom images
top_image_clip = ImageClip(top_image_path).set_duration(10).resize(height=image_height).set_position(("center", y_coordinate - (image_height * 0.75))).crossfadein(1).set_start(top_start_time)
bottom_image_clip = ImageClip(bottom_image_path).set_duration(10).resize(height=image_height).set_position(("center", y_coordinate + (image_height * 0.75))).crossfadein(1).set_start(bottom_start_time)

# Create text clips for bottom, top and middle text
txt_clip_top = TextClip(top_text, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_duration(video_duration).set_position(("center", 50)).set_start(top_start_time)
txt_clip_bottom = TextClip(bottom_text, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana', method='caption').set_duration(video_duration).set_position(("center", 1750)).set_start(bottom_start_time)
# txt_clip_center = TextClip(transcription['text'], fontsize=50, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_position(("center", "center")).set_duration(10);

# add audios
voice_over = AudioFileClip(voiceover_filepath)
gasp = AudioFileClip("audio/gasp.mp3")
background_music = AudioFileClip('audio/byebye.mp3').volumex(0.15)

while background_music.duration < video_duration: # repeat the background music if it's shorter than the video
    background_music = concatenate_audioclips([background_music, background_music])

background_music = background_music.set_duration(video_duration)

combined_audio = concatenate_audioclips([voice_over, gasp]).set_end(video_duration)
final_composite_audio = CompositeAudioClip([combined_audio, background_music])

# Overlay all clips on the first clip
final_clip = CompositeVideoClip([background_clip, top_image_clip, bottom_image_clip, txt_clip_top, txt_clip_bottom]).set_audio(final_composite_audio).set_duration(video_duration)

# Write the result to a file
final_clip.write_videofile(output, fps=24)