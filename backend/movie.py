# from parse import captions
# from moviepy.video.fx.all import fadein, resize
# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip
# import os


# # Set FFmpeg path manually inside Conda environment
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/anaconda3/envs/mana/bin/ffmpeg"
# os.environ["IMAGEMAGICK_BINARY"] = "/opt/homebrew/bin/magick"

# # YouTube Shorts resolution
# SHORTS_WIDTH, SHORTS_HEIGHT = 1080, 1920
# PADDING = 50  # Padding for summary image

# MAX_DURATION = captions[-1][1]

# # Create a red background with YouTube Shorts resolution
# background = ColorClip(size=(SHORTS_WIDTH, SHORTS_HEIGHT),
#                        color=(10, 6, 47)).set_duration(MAX_DURATION)

# # ✅ Ensure Corgi GIF exists before loading
# corgi_path = "./assets/corgi.gif"
# if not os.path.exists(corgi_path):
#     raise FileNotFoundError(f"❌ Corgi GIF not found at {corgi_path}")

# video = VideoFileClip(corgi_path, has_mask=True)

# # Loop the 2-second GIF to play for 10 seconds
# looped_video = video.loop(duration=MAX_DURATION)

# # ✅ Start from small size and grow to exactly 700px height
# initial_height = 100  # Start very small
# final_height = 700  # Target size

# # Get original aspect ratio to maintain proportions
# aspect_ratio = video.w / video.h

# # ✅ Avoid double resize → Directly apply smooth scaling


# def scale_func(t):
#     if t > 0.3:
#         # Exact target size
#         return (final_height, int(final_height * aspect_ratio))
#     else:
#         scale_factor = (t / 0.3)  # Linear scaling
#         return (int(initial_height + scale_factor * (final_height - initial_height)),  # Height interpolation
#                 int((initial_height + scale_factor * (final_height - initial_height)) * aspect_ratio))  # Width interpolation


# gif_resized = looped_video.set_position((-65, "bottom")).resize(scale_func)

# # ✅ Ensure Trend Image exists before loading
# trend_img_path = "images/1740258865.png"
# if not os.path.exists(trend_img_path):
#     raise FileNotFoundError(f"❌ Trend Image not found at {trend_img_path}")

# trend_img = ImageClip(trend_img_path).resize(
#     width=SHORTS_WIDTH - 2 * PADDING)  # Add padding on sides
# trend_img = trend_img.set_position(
#     ("center", "center")).set_duration(MAX_DURATION)

# # ✅ Apply delayed pop-in (Ensures trend image appears after Corgi)
# trend_img = trend_img.resize(lambda t: max(
#     0.5, min(1, t * 2.5)) if t < 0.8 else 1).set_start(0.5)

# # ✅ Ensure Audio exists before loading
# audio_path = "process_transcription/1740258144.wav"
# if not os.path.exists(audio_path):
#     raise FileNotFoundError(f"❌ Audio file not found at {audio_path}")

# audio = AudioFileClip(audio_path).set_duration(MAX_DURATION)

# # ✅ Define captions (text + timestamps)

# print(captions)


# # ✅ Choose a cool news-style font
# # Impact is a bold, news-style font
# font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"

# # ✅ Properly place captions ABOVE the trend image
# trend_img_height = SHORTS_HEIGHT // 3  # Approximate size for centering
# # Adjusted manually for visibility
# subtitle_y_position = (SHORTS_HEIGHT // 2) - (trend_img_height // 2) - 500

# # ✅ Generate text clips for captions above the centered image
# subtitle_clips = [
#     TextClip(text, fontsize=100, color="white", font=font_path,
#              stroke_width=3, stroke_color="black")
#     .set_position(("center", subtitle_y_position))  # ✅ Fixed placement
#     .set_start(start)
#     .set_end(end)
#     for start, end, text in captions
# ]


# # ✅ Layer subtitles AFTER the trend image to ensure they appear above it
# final_video = CompositeVideoClip(
#     [background, trend_img, gif_resized,  *subtitle_clips]).set_audio(audio)

# # ✅ Save the final edited video with high quality
# final_video.write_videofile(
#     "output_shorts.mp4", codec="libx264", fps=24, audio_codec="aac", bitrate="5000k")

# # Close video and audio files
# video.close()
# final_video.close()
# audio.close()
from parse import captions
import os
from moviepy.video.fx.all import fadein, resize
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip

# Set FFmpeg path manually inside Conda environment
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/anaconda3/envs/mana/bin/ffmpeg"
os.environ["IMAGEMAGICK_BINARY"] = "/opt/homebrew/bin/magick"

# Directory where processed files are stored
transcription_dir = "process_transcription"
image_path = 'images'

# ✅ Find the latest text file for captions
text_files = [f for f in os.listdir(transcription_dir) if f.endswith(".txt")]
if not text_files:
    raise FileNotFoundError("❌ No text files found in process_transcription")

latest_text_file = max(text_files, key=lambda f: os.path.getctime(
    os.path.join(transcription_dir, f)))
text_filepath = os.path.join(transcription_dir, latest_text_file)

# ✅ Extract filename (without extension) to find matching files
filename, _ = os.path.splitext(latest_text_file)

# ✅ Load corresponding audio file (.wav)
audio_filepath = os.path.join(transcription_dir, f"{filename}.wav")
if not os.path.exists(audio_filepath):
    raise FileNotFoundError(f"❌ Audio file {audio_filepath} not found")

# ✅ Load corresponding image file (.png)
image_filepath = os.path.join(image_path, f"{filename}.png")
if not os.path.exists(image_filepath):
    raise FileNotFoundError(f"❌ Image file {image_filepath} not found")

# YouTube Shorts resolution
SHORTS_WIDTH, SHORTS_HEIGHT = 1080, 1920
PADDING = 50  # Padding for summary image
MAX_DURATION = captions[-1][1]  # Adjust based on content
print(captions)
print('max', MAX_DURATION)

# Create a background color
background = ColorClip(size=(SHORTS_WIDTH, SHORTS_HEIGHT),
                       color=(10, 6, 47)).set_duration(MAX_DURATION)

# ✅ Ensure Corgi GIF exists before loading
corgi_path = "./assets/corgi.gif"
if not os.path.exists(corgi_path):
    raise FileNotFoundError(f"❌ Corgi GIF not found at {corgi_path}")

video = VideoFileClip(corgi_path, has_mask=True)

# Loop the 2-second GIF to play for MAX_DURATION
looped_video = video.loop(duration=MAX_DURATION)

# ✅ Rescale the GIF to 700px height
gif_resized = looped_video.set_position(
    ("center", "bottom")).resize(height=700)

# ✅ Load the trend image (from process_transcription)
trend_img = ImageClip(image_filepath).resize(width=SHORTS_WIDTH - 2 * PADDING)
trend_img = trend_img.set_position(
    ("center", "center")).set_duration(MAX_DURATION)

# ✅ Apply delayed pop-in effect
trend_img = trend_img.resize(lambda t: max(
    0.5, min(1, t * 2.5)) if t < 0.8 else 1).set_start(0.5)

# ✅ Load the audio file
audio = AudioFileClip(audio_filepath).set_duration(MAX_DURATION)

# ✅ Choose a bold font for captions
font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"

# ✅ Properly place captions ABOVE the trend image
trend_img_height = SHORTS_HEIGHT // 3  # Approximate size for centering
# Adjusted manually for visibility
subtitle_y_position = (SHORTS_HEIGHT // 2) - (trend_img_height // 2) - 500

# ✅ Generate text clips for captions above the centered image
subtitle_clips = [
    TextClip(text, fontsize=100, color="white", font=font_path,
             stroke_width=3, stroke_color="black")
    .set_position(("center", subtitle_y_position))  # ✅ Fixed placement
    .set_start(start)
    .set_end(end)
    for start, end, text in captions
]

# ✅ Final video composition
final_video = CompositeVideoClip(
    [background, trend_img, gif_resized, *subtitle_clips]
).set_audio(audio)

# ✅ Save the final edited video
final_video.write_videofile(
    "output_shorts.mp4", codec="libx264", fps=24, audio_codec="aac", bitrate="5000k"
)

# Close video and audio files
video.close()
final_video.close()
audio.close()
