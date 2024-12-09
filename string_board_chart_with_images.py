# set the linking random based on the number of images, not all images are linked

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import random

# Function to download an image from a URL
def download_image(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    content_type = response.headers['Content-Type']
    if 'image' in content_type:
        image = Image.open(BytesIO(response.content))
        image.save(save_path)
    else:
        raise ValueError(f"URL does not point to an image: {url}")

# Function to add an image to the plot
def add_image(ax, img_path, xy, zoom=0.1):
    img = plt.imread(img_path)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, xy,
                        xybox=(0, 0),
                        boxcoords="offset points",
                        pad=0)
    ax.add_artist(ab)

# Directory to save images
dir_start = Path('./sample_data/')
dir_start.mkdir(parents=True, exist_ok=True)

# Image URLs (can be extended with many images)
image_links = [
    'https://img.freepik.com/premium-photo/chinese-baby-boy-as-concept-chinese-new-year-happy-cute-asian-infant-baby-sitting-smiling_641698-1079.jpg',
    'https://st3.depositphotos.com/1177973/12758/i/450/depositphotos_127589406-stock-photo-african-american-girl.jpg',
    'https://media.istockphoto.com/id/969921038/photo/happy-little-girl-laughing-and-smiling-outside.webp?b=1&s=612x612&w=0&k=20&c=wIKwuBU7hB88OwFlxY44S3LHy7JLOcZgp8oub9I7VTA=',
    'https://wallpapersok.com/images/high/cute-boy-wearing-white-shirt-jalyev4iyirsnsz5.webp', 
    'https://qph.cf2.quoracdn.net/main-qimg-d831efca00b819e09c4fc362d7ab16f8-lq'
]

# Placeholder image (in case of failure)
placeholder_image = ''
placeholder_path = dir_start / 'placeholder.png'
download_image(placeholder_image, placeholder_path)

# Download images and handle errors
image_paths = []
for i, url in enumerate(image_links):
    img_path = dir_start / f'image_{i:02d}.jpg'
    try:
        download_image(url, img_path)
        image_paths.append(img_path)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        image_paths.append(placeholder_path)

# Generate random positions for images
num_images = len(image_paths)
positions = [(random.randint(0, 4), random.randint(0, 4)) for _ in range(num_images)]

"""
# Example data linking positions and images
data = {
    'A': {'pos': (1, 3), 'img': image_paths[0]},
    'B': {'pos': (2, 1), 'img': image_paths[1]},
    'C': {'pos': (3, 2), 'img': image_paths[2]},
}
"""
# Example data linking positions and images dynamically
data = {}
for i, pos in enumerate(positions):
    data[chr(65 + i)] = {'pos': pos, 'img': image_paths[i]}

# Set random links (not all images need to be linked)
num_links = random.randint(1, num_images * (num_images - 1) // 2)
all_pairs = [(i, j) for i in range(num_images) for j in range(i + 1, num_images)]
random_links = random.sample(all_pairs, num_links)

# Create the plot
fig, ax = plt.subplots()

# Define the separate data names for labeling
data_names = ['X', 'Y', 'Z', 'W', 'V']  # List of names for tags

# Plot data points and add images
for label, info in data.items():
    pos = info['pos']
    img_path = info['img']
    ax.plot(pos[0], pos[1], 'o', label=label)
    add_image(ax, img_path, pos, zoom=0.1)

# Draw random links between images
for (i, j) in random_links:
    x1, y1 = data[chr(65 + i)]['pos']
    x2, y2 = data[chr(65 + j)]['pos']
    ax.plot([x1, x2], [y1, y2], 'r-', lw=2)  # Red line

# Tag images with names from the data_names list
for i in range(len(data)):
    x, y = data[chr(65 + i)]['pos']
    #ax.text(x, y, data_names[i], fontsize=12, ha='center', va='center', color='black')
    ax.text(x - 0.5, y + 0.5, data_names[i], fontsize=12, ha='left', va='top', color='black')
    #ax.text(x, y, data_names[i], fontsize=12, ha='left', va='top', color='black')

# Set plot limits with offset
x_min = min(data[chr(65 + i)]['pos'][0] for i in range(len(data)))
x_max = max(data[chr(65 + i)]['pos'][0] for i in range(len(data)))
y_min = min(data[chr(65 + i)]['pos'][1] for i in range(len(data)))
y_max = max(data[chr(65 + i)]['pos'][1] for i in range(len(data)))

# Apply an offset of 1
ax.set_xlim(x_min - 1, x_max + 1)
ax.set_ylim(y_min - 1, y_max + 1)
ax.legend()

# Display the plot
plt.show()

