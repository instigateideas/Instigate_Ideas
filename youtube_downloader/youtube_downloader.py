import pytube
import ffmpeg
import os
import glob
import json
from flask import Flask, request

app = Flask(__name__)

@app.route("/download_youtube", methods=['GET', 'POST'])
def index():
	data = request.get_data()
	jdata = json.loads(data)
	# link = input("enter the youtube url: ")
	link = jdata["url"]
	download_path = jdata["path"]
	yt = pytube.YouTube(link)
	base_path = download_path
	download_from_youtube(base_path=base_path, obj_yt=yt)

def create_directory(path):
	try:
		os.makedirs(path)
	except OSError:
		print ("Creation of the directory %s failed" % path)
	else:
		print ("Successfully created the directory %s" % path)

def delete_directory(path):
	try:
		cmd = "rm -rf {}".format(path)
		os.command(cmd)
	except OSError:
		print ("Deletion of the directory %s failed" % path)
	else:
		print ("Successfully deleted the directory %s" % path)

def get_file_name(path):
	return glob.glob(path+"/*")[0]

def get_quality_streams(yt):
	prog_video = yt.streams.filter(type="video", progressive=True, file_extension='mp4').order_by('resolution').desc().first()
	adap_video = yt.streams.filter(type="video", adaptive=True, file_extension='webm').order_by('resolution').desc().first()
	adap_audio = yt.streams.filter(type="audio", adaptive=True, file_extension='webm').order_by('abr').desc().first()

	return {"Progressive": prog_video, "Adaptive": {"adap_video": adap_video, "adap_audio": adap_audio}}

def get_video_details(yt):
	#Showing details
	yt_title = yt.title
	print("Title: ", yt_title)
	yt_views = yt.views
	print("Number of views: ",yt_views)
	yt_length = yt.length
	print("Length of video: ",yt_length)
	yt_rating = yt.rating
	print("Rating of video: ",yt_rating)
	yt_thumb = yt.thumbnail_url
	print("Thumbnail of video: ",yt_thumb)

	return {"title": yt_title}

def youtube_download(stream_selected, path):
	stream_selected.download(output_path=path)

def check_and_download(base_path, stream):
	video_path = base_path+"/video"
	audio_path = base_path+"/audio"
	if stream["Adaptive"]["adap_video"] != None:
		print("Downloading the Adaptive Streaming Video..")
		create_directory(path=video_path)
		create_directory(path=audio_path)
		youtube_download(stream_selected = stream["Adaptive"]["adap_video"], path=video_path)
		youtube_download(stream_selected = stream["Adaptive"]["adap_audio"], path=audio_path)
		file_name = get_file_name(video_path).split("/")[-1]
		video_stream = ffmpeg.input(get_file_name(video_path))
		audio_stream = ffmpeg.input(get_file_name(audio_path))
		output_path = base_path + "/"+ file_name
		ffmpeg.output(audio_stream, video_stream, output_path).run()
		delete_directory(video_path)
		delete_directory(audio_path)
	else:
		create_directory(path=base_path)
		youtube_download(stream_selected = stream["Progressive"], path=base_path)


def download_from_youtube(base_path, obj_yt):
	streams = get_quality_streams(yt=obj_yt)
	check_and_download(base_path=base_path, stream=streams)



if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5001)
    # optional if we want to run in debugging mode
    app.run(debug=True)

