from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
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


def slice_video(video_name, index_file, intro, outro):
    """
    Cuts video in the parts described in the index file
    """
    clip_c = VideoFileClip(video_name)
    if intro or outro:
        intro_clip = VideoFileClip("videos/thedojo_intro.mp4")
        outro_clip = VideoFileClip("videos/thedojo_outro.mp4")
    duration = clip_c.duration

    print(duration)
    timestamps = []

    with open(index_file, "r") as f:
        reader = csv.reader(
            f, quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True
        )
        for line in reader:
            time_range = (stamp_to_seconds(line[0]), stamp_to_seconds(line[1]))
            # time_end = (stamp_to_seconds(line[1]),)
            timestamps.append(
                [
                    line[2].strip(),
                    int(line[3].strip()),
                    stamp_to_seconds(line[0]),
                    stamp_to_seconds(line[1]),
                ]
            )

    print(timestamps)
    # Creating folders
    video_unique_name = video_name.split(".")[-2].split("/")[-1]
    destination_folder = "videos/{}".format(video_unique_name)
    try:
        os.makedirs(destination_folder + "/cuts")
        os.makedirs(destination_folder + "/final")
    except Exception as e:
        print(e)

    for ts in timestamps:
        if not ts[1]:
            print("------------------")
            print("Skipping " + ts[0])
            print("------------------")
            continue
        print("Slicing: " + ts[0])

        cut_video_name = "{}/cuts/{}.mp4".format(destination_folder, ts[0])
        print(video_name, ts[2], ts[3], cut_video_name)
        # ffmpeg_extract_subclip(video_name, ts[2], ts[3], targetname=cut_video_name)
        clip = clip_c.subclip(ts[2], ts[3])
        clip.write_videofile(
            cut_video_name, fps=30, preset="ultrafast", threads=16
        )
        if intro or outro:

            final_name = "{}/final/{}.mp4".format(destination_folder, ts[0])

            clip = VideoFileClip(cut_video_name)
            d = clip.duration
            # clip = vfx.fadeout(clip, duration=5)
            clip = clip.set_duration(d - 4)
            final_clip = concatenate_videoclips(
                [intro_clip, clip, outro_clip, intro_clip], padding=1
            )
            final_clip.write_videofile(
                final_name, fps=30, preset="ultrafast", threads=8
            )
            final_clip.close()
            clip.close()
    clip_c.close()
    if intro or outro:
        intro_clip.close()
        outro_clip.close()


@begin.start
def run(
    video_name="videos/dt.mp4",
    index_file="videos/dt/index.csv",
    intro=False,
    outro=False,
):
    slice_video(video_name, index_file, intro, outro)