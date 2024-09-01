from IPython.display import display, Video, Image as IPImage
import moviepy.editor as mpy
import os
import time
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# Load the model (using Stable Diffusion as an example)
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
pipe = pipe.to("cuda")  # Use GPU if available

# Prompt user for input
text_prompt = input("Enter any sentence: ")

# Generate the image
image = pipe(text_prompt).images[0]

# Display the image in the notebook
display(image)

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

# Display the video in the notebook
try:
    video_path = "output_video.mp4"
    display(Video(video_path))
except Exception as e:
    print("Video display failed, displaying images frame by frame instead.")
    # Fallback: Display images frame by frame if video fails to display
    for i in range(10):
        img_path = f"{output_dir}/frame_{i:03d}.png"
        display(IPImage(filename=img_path))
        time.sleep(1)
