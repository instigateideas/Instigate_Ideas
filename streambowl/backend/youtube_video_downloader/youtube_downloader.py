from pytube import YouTube
import ffmpeg
import subprocess
import os

youtube_video_download_path = "/home/arunachalam/Documents/output_streambowl/youtube"

def video_downloader(youtube_video_id, output_path):
	#ask for the link from user
	# link = input("Enter the link of YouTube video you want to download:  ")
	youtube_link="https://www.youtube.com/watch?v={}".format(youtube_video_id)
	yt = YouTube(youtube_link)

	#Showing details
	print("Title: ",yt.title)
	print("Number of views: ",yt.views)
	print("Length of video: ",yt.length)
	print("Rating of video: ",yt.rating)

	# Getting the highest resolution possible
	# ys = yt.streams.get_highest_resolution()
	yt_video = yt.streams.filter(progressive=False, resolution="1080p", file_extension='mp4').order_by('resolution').desc().first()
	print(yt_video)
	yt_audio=yt.streams.filter(only_audio=True, file_extension='mp4').order_by("abr").desc().first()
	print(yt_audio)


	# Starting download
	print("Starting Download...")
	video_file_prefix="{}_id_video_".format(youtube_video_id)
	edited_video_title = clean_up_title(title=yt.title)
	video_saved_path = yt_video.download(output_path=output_path, filename=edited_video_title, filename_prefix=video_file_prefix)
	print(video_saved_path)
	audio_file_prefix="{}_id_audio_".format(youtube_video_id)
	print("Download Youtube Video completed!!")
	audio_saved_path = yt_audio.download(output_path=output_path, filename=edited_video_title, filename_prefix=audio_file_prefix)
	print(audio_saved_path)
	print("Download Youtube Audio completed!!")
	mix_audio_video(audio_file=audio_saved_path, video_file=video_saved_path, video_title=edited_video_title, video_id=youtube_video_id, output_path=output_path)
	print("Saved the mixed file")

def clean_up_title(title):
	title = title.replace(" ", "_")
	title = title.replace("|", "")
	title = title.replace(",", "")

	return title

def mix_audio_video(audio_file, video_file, video_title, output_path, video_id):
	input_video = ffmpeg.input(video_file)
	input_audio = ffmpeg.input(audio_file)
	output_file_name = "./{}/{}_proc_{}.mp4".format("output", video_id, video_title)
	print(output_file_name)
	cmd_input = f"ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac -ab {output_file_name}"
	subprocess.run(cmd_input, shell=True)
	#ffmpeg.concat(input_video, input_audio, v=1, a=1).output("./finished_video.mp4").run()

video_downloader(youtube_video_id="YFYiTS46x-8", output_path=youtube_video_download_path)