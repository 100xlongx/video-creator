import os
from bing_image_downloader import downloader

output_dir = 'assets'

def get_image_path(topic, output_dir):
    directory = f"{output_dir}/{topic.replace(' ', ' ')}"  # Adjusted for spaces in topic
    files = os.listdir(directory)
    if files:
        # Assuming the first image is the one we want, adjust as needed
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Checking for common image types
                return os.path.join(directory, file)
    return None  # or handle this case as needed

def create_image_path_from_keyword(keyword):
    # fetch image from bing and download it
    downloader.download(keyword, limit=1, output_dir=output_dir, force_replace=False, timeout=60, verbose=True)
    image_path = get_image_path(keyword, output_dir)

    return image_path
