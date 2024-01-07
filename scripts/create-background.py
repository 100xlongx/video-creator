import numpy as np
import cv2  # OpenCV

# Define your frame size - typical for TikTok 9:16 ratio
width, height = 1080, 1920

# Calculate the heights of each section
red_height = int(height * 0.49)
black_height = int(height * 0.02)
blue_height = height - red_height - black_height  # Remainder to blue to avoid rounding errors

# Create the three sections using numpy
red_square = np.full((red_height, width, 3), (0, 0, 255), dtype=np.uint8)  # RGB for red
black_line = np.zeros((black_height, width, 3), dtype=np.uint8)  # RGB for black
blue_square = np.full((blue_height, width, 3), (255, 0, 0), dtype=np.uint8)  # RGB for blue

# Stack them vertically
background = np.vstack((red_square, black_line, blue_square))

# Display the image using OpenCV
cv2.imshow('Background', background)
cv2.waitKey(0)  # Wait for keypress to close
cv2.destroyAllWindows()

# Save the image
cv2.imwrite('assets/tiktok_background.jpg', background)
