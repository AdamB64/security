from moviepy.editor import VideoFileClip

# Load the video file
video_path = r"C:/Users/adam2/Videos/2024-04-16 13-01-32.mkv"
video_clip = VideoFileClip(video_path)

# Increase the volume by a factor (e.g., 2 for doubling the volume)
volume_factor = 6
video_clip = video_clip.volumex(volume_factor)

# Write the modified video to a new file
output_path = r"C:/Users/adam2/Videos/output_video.mp4"
video_clip.write_videofile(output_path)

# Close the video clip
video_clip.close()
