from PIL import Image
import os
import time
from diffusers import StableDiffusionPipeline
import torch
import moviepy.editor as mpy

# Load the model (using Stable Diffusion as an example)
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
pipe = pipe.to("cuda")  # Use GPU if available

# Prompt user for input
text_prompt = input("Enter any sentence: ")

# Generate the image
image = pipe(text_prompt).images[0]

# Display the image using PIL's built-in viewer
image.show()

# Save the image
image.save("output_image.png")


# Create a directory to store the frames
output_dir = "video_frames"
os.makedirs(output_dir, exist_ok=True)

# Generate a sequence of images (frames) for the video
user_prompt = input("Enter a sentence for video frames: ")
for i in range(10):
    frame_prompt = f"{user_prompt}, frame {i}"
    image = pipe(frame_prompt).images[0]
    image.save(f"{output_dir}/frame_{i:03d}.png")

# Create a video from the generated frames
image_files = [f"{output_dir}/frame_{i:03d}.png" for i in range(10)]
video_clip = mpy.ImageSequenceClip(image_files, fps=2)  # Adjust FPS as needed
video_clip.write_videofile("output_video.mp4", codec="libx264")

# Play the video using the default system video player
os.system("start output_video.mp4")  # On Windows
# For macOS, you would use: os.system("open output_video.mp4")
# For Linux, you would use: os.system("xdg-open output_video.mp4")
