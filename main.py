from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip, concatenate_audioclips
from dotenv import load_dotenv
from openai_wrapper import OpenAIWrapper
from helpers import create_image_path_from_keyword
import argparse
import os

load_dotenv()

background_width, background_height, image_height = 1080, 1920, 600
y_coordinate = (background_height - image_height) // 2

parser = argparse.ArgumentParser(description="Video Creation Tool")

parser.add_argument("-tt", "--top_text", required=True, help="The top text")
parser.add_argument("-tp", "--top_prompt", help="Enter the top prompt (optional, defaults to top text if not provided)")
parser.add_argument("-bt", "--bottom_text", required=True, help="Enter the bottom text")
parser.add_argument("-bp", "--bottom_prompt", help="Enter the bottom prompt (optional, defaults to bottom text if not provided)")
parser.add_argument("-vf", "--voiceover_file", required=False, help="Path to the voiceover audio file (will use openAI to create one if not provided)")
parser.add_argument("-o", "--output", required=False, help="Output file path")

args = parser.parse_args()

# Calculate the y-coordinate for centering the image vertically

top_topic = args.top_text
bottom_topic = args.bottom_text

top_prompt = args.top_prompt if args.top_prompt is not None else top_topic
bottom_prompt = args.bottom_prompt if args.bottom_prompt is not None else bottom_topic

output = args.output if args.output is not None else f"output/{top_topic.replace(' ', '_')}-{bottom_topic.replace(' ', '_')}.mp4"

if args.voiceover_file is not None:
    voiceover_filepath = args.voiceover_file
else:
    openai_wrapper = OpenAIWrapper(os.getenv("OPENAI_API_KEY"))

    voiceover_filepath = openai_wrapper.generate_speech(
        f"Would you rather pick {top_topic} or {bottom_topic}?",
        file_path=f"audio/{top_topic.replace(' ', '_')}-{bottom_topic.replace(' ', '_')}.mp3"
    )

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
txt_clip_top = TextClip(top_prompt, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_duration(video_duration).set_position(("center", 50)).set_start(top_start_time)
txt_clip_bottom = TextClip(bottom_prompt, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Verdana', method='caption').set_duration(video_duration).set_position(("center", 1750)).set_start(bottom_start_time)
# txt_clip_center = TextClip(transcription['text'], fontsize=50, color='white', stroke_color='black', stroke_width=2, font='Verdana').set_position(("center", "center")).set_duration(10);

# add audios
voice_over = AudioFileClip(voiceover_filepath)
gasp = AudioFileClip("audio/gasp.mp3")
background_music = AudioFileClip('audio/byebye.mp3').volumex(0.15)

while background_music.duration < video_duration:
    background_music = concatenate_audioclips([background_music, background_music])

background_music = background_music.set_duration(video_duration)

final_audio = concatenate_audioclips([voice_over, gasp]).set_end(video_duration)
composite_audio = CompositeAudioClip([final_audio, background_music])

# Overlay all clips on the first clip
final_clip = CompositeVideoClip([background_clip, top_image_clip, bottom_image_clip, txt_clip_top, txt_clip_bottom]).set_audio(composite_audio).set_duration(video_duration)

# Write the result to a file
final_clip.write_videofile(output, fps=24)