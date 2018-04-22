#!/usr/bin/env python

import VideoChunkDownloader as vcd
import VideoServer as vs
from threading import Thread
from flask import Flask, request
app = Flask(__name__)

HTTP_200_OK = 200
FORMAT_640x360 = '93'

def download_video_chunks(downloader, youtube_link, desired_format, video_output_path):
   downloader.start(youtube_link, desired_format, video_output_path)

def serve_video(server, path_to_serve, port):
   server.start(path_to_serve, port)

@app.route("/start_app", methods = ['POST'])
def start_app():
   payload = request.get_json(force = True)
   youtube_link = payload['youtube_url']
   path_for_video = payload['video_path']
   serve_video_port = payload['serve_port']

   print 'Starting with youtube URL: ' + youtube_link
   print 'Storing video at: ' + path_for_video
   print 'Serving video on port: ' + str(serve_video_port)

   downloader = vcd.VideoChunkDownloader()
   server = vs.VideoServer()
   video_download_thread = (
      Thread(target = download_video_chunks, args = (downloader, youtube_link, FORMAT_640x360, path_for_video,)))
   video_download_thread.daemon = True
   video_server_thread = (
      Thread(target = serve_video, args = (server, path_for_video, serve_video_port,)))
   video_server_thread.daemon = True
   video_download_thread.start()
   video_server_thread.start()

   return 'Success', HTTP_200_OK