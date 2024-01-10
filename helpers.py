import os
import hashlib
import requests
from PIL import Image
from io import BytesIO
from bing_image_downloader import downloader

assets_directory = 'assets'

def get_image_path(topic: str, output_dir: str) -> str:
    directory = f"{output_dir}/{topic.replace(' ', ' ')}"  # Adjusted for spaces in topic
    files = os.listdir(directory)
    if files:
        # Assuming the first image is the one we want, adjust as needed
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Checking for common image types
                return os.path.join(directory, file)
    return None  # or handle this case as needed

def create_image_path_from_keyword(keyword: str, image_source: str, manual_image_url: str = None) -> str:
    if image_source == 'manual':
        if manual_image_url is None:
            raise ValueError("No URL provided for manual image download.")
        return download_image_from_url(manual_image_url, f"{assets_directory}/manual_images")
    elif image_source == 'bing':
        output_dir = f"{assets_directory}/bing_images"
        downloader.download(keyword, limit=1, output_dir=output_dir, force_replace=False, timeout=60, verbose=True)
        return get_image_path(keyword, output_dir)
    elif image_source == 'dalle':
        raise Exception("DALL-E not implemented yet")
    else:
        raise Exception("Invalid image source")

def download_image_from_url(url: str, output_dir: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        file_path = os.path.join(output_dir, os.path.basename(url))
        image.save(file_path)
        return file_path
    else:
        raise Exception(f"Failed to download image from {url}")
    
def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# Check if the voice over file exists, if not, create it.
def check_if_voice_over_exists(filename: str, output_dir = "audio/voice_overs/") -> bool:
    file_path = os.path.join(output_dir, filename + ".mp3")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return os.path.isfile(file_path)