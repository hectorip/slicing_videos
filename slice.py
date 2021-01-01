from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
from moviepy.editor import VideoFileClip
import csv
clip = VideoFileClip("videos/dt.mp4")
duration =  clip.duration

print(duration)
timestamps = []


def stamp_to_seconds(ts):
    seconds = 0
    parts = ts.split(":")
    parts.reverse()

    seconds_per_unit = [1, 60, 3600, 86400]
    unit = 0
    for p in parts:
        seconds += int(p) * seconds_per_unit[unit]
        unit += 1
    return seconds

with open("v1.csv", "r") as f:
    # print(f.read())
    reader = csv.reader(f)
    for line in reader:
        time_start = stamp_to_seconds(line[0])
        timestamps.append([line[1].strip(), time_start])


l = len(timestamps)
for i, ts in enumerate(timestamps[:-1]):
    time_end = timestamps[i+1][1] - 1
    ts.append(time_end)

print(timestamps)
# ffmpeg_extract_subclip("full.mp4", 60, 300, targetname="cut.mp4")


