from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from bing_image_downloader import downloader
import os

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

output_video_path = f'output/{top_topic}-{bottom_topic}.mp4'

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
txt_clip_top = TextClip(top_topic, fontsize=70, color='white').set_position(("center", "top")).set_duration(10)

# Create a TextClip object for bottom text
txt_clip_bottom = TextClip(bottom_topic, fontsize=70, color='white').set_position(("center", "bottom")).set_duration(10)

# Overlay the text clips on the image clips
# You might want to adjust the position based on the size and position of your images
txt_clip_top = txt_clip_top.set_position(("center", 50))
txt_clip_bottom = txt_clip_bottom.set_position(("center", 1750))  # Adjust based on your video height

# Overlay all clips on the first clip
final_clip = CompositeVideoClip([background_clip, top_image_clip, bottom_image_clip, txt_clip_top, txt_clip_bottom])

# Write the result to a file
final_clip.write_videofile(output_video_path, fps=24)