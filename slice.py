from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import csv
import moviepy.audio.fx.all as afx
import begin
import os


def stamp_to_seconds(ts):
    """
    Transforms from a string in form [dd:][hh:]mm:ss to its equivalent
    in seconds
    """
    seconds = 0
    parts = ts.split(":")
    parts.reverse()

    seconds_per_unit = [1, 60, 3600, 86400]
    unit = 0
    for p in parts:
        seconds += int(p) * seconds_per_unit[unit]
        unit += 1
    return seconds

def slice_video(video_name, index_file):
    clip_c = VideoFileClip(video_name)
    intro_clip = VideoFileClip("videos/thedojo_intro.mp4")
    duration =  clip_c.duration

    print(duration)
    timestamps = []

    with open(index_file, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            time_start = stamp_to_seconds(line[0])
            timestamps.append([line[1].strip(), int(line[2].strip()), time_start])


    l = len(timestamps)
    for i, ts in enumerate(timestamps[:-1]):
        time_end = timestamps[i+1][2] - 1
        ts.append(time_end)

    timestamps[-1].append(duration)
    print(timestamps)
    # Creating folders
    video_unique_name = video_name.split(".")[-2].split("/")[-1]
    destination_folder = "videos/{}".format(video_unique_name)
    os.makedirs(destination_folder + "/cuts")
    os.makedirs(destination_folder + "/final")

    for ts in timestamps:
        if not ts[1]:
            print("------------------")
            print("Skipping " + ts[0])
            print("------------------")
            continue
        print("Slicing: " + ts[0])

        cut_video_name = "{}/cuts/{}.mp4".format(destination_folder, ts[0])
        final_name = "{}/final/{}.mp4".format(destination_folder, ts[0])
        ffmpeg_extract_subclip(video_name, ts[2], ts[3], targetname=cut_video_name)
        clip = VideoFileClip(cut_video_name)
        clip = vfx.fadeout(clip, duration=5)
        clip = afx.audio_fadeout(clip, duration=5)
        # clip.write_videofile("t1.mp4", fps=30, preset="ultrafast", )
        final_clip = concatenate_videoclips([intro_clip, clip])
        final_clip = final_clip.set_duration(final_clip.duration-4.2)
        final_clip.write_videofile(final_name, fps=24, preset="medium", threads=24, codec="libx264")
        final_clip.close()
        clip.close()
        # exit()
    clip_c.close()
    intro_clip.close()


@begin.start
def run(video_name="videos/dt.mp4", index_file="videos/dt/index.csv"):
    slice_video(video_name, index_file)