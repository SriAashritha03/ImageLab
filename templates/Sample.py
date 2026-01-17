import cv2
import os
import numpy as np

# 1. Load the image
img = cv2.imread(r"D:\VRSU\Images\Teddy.jpg")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply median blur to reduce noise
gray = cv2.medianBlur(gray, 5)

# Detect edges using adaptive threshold
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

# Apply bilateral filter to smooth the image
color = cv2.bilateralFilter(img, 9, 300, 300)

# Combine the smoothed image with the edges to create cartoon effect
cartoon = cv2.bitwise_and(color, color, mask=edges)

# 3. Define the output path
output_folder = r"D:\Image-dashboard\static\previews"
output_filename = "cartoon_teddy.jpg"
full_output_path = os.path.join(output_folder, output_filename)

# Ensure the directory exists
os.makedirs(output_folder, exist_ok=True)

# 4. Save the cartoon image
cv2.imwrite(full_output_path, cartoon)

print(f"Cartoon image saved to: {full_output_path}")
