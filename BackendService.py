#!/usr/bin/env python

import VideoChunkDownloader as vcd
import VideoServer as vs
import PdfSlidesService as pss
from threading import Thread
from flask import Flask, request
app = Flask(__name__)

HTTP_200_OK = 200
FORMAT_720 = '94'

def download_video_chunks(downloader, youtube_link, desired_format, video_output_path):
   downloader.start(youtube_link, desired_format, video_output_path)

def serve_video(server, path_to_serve, port):
   server.start(path_to_serve, port)

def start_pdf_conversion(pdf, input_path, output_path):
   pdf.start(input_path, output_path)

@app.route("/start_app", methods = ['POST'])
def start_app():
   payload = request.get_json(force = True)
   youtube_link = payload['youtube_url']
   path_for_video = payload['video_path']
   serve_video_port = payload['serve_port']
   path_for_input_pdf_slides = payload['input_slides_path']
   path_for_jpg_slides = payload['output_slides_path']

   print 'Starting with youtube URL: ' + youtube_link
   print 'Storing video at: ' + path_for_video
   print 'Serving video on port: ' + str(serve_video_port)
   print 'Getting pdf slides from: ' + path_for_input_pdf_slides
   print 'Saving output jpg slides at: ' + path_for_jpg_slides

   downloader = vcd.VideoChunkDownloader()
   downloader.clear_stale_data(path_for_video)
   server = vs.VideoServer()
   pdf = pss.PdfSlidesService()
   pdf.clear_stale_data(path_for_jpg_slides)

   video_download_thread = (
      Thread(target = download_video_chunks, args = (downloader, youtube_link, FORMAT_720, path_for_video,)))
   video_download_thread.daemon = True
   video_server_thread = (
      Thread(target = serve_video, args = (server, path_for_video, serve_video_port,)))
   video_server_thread.daemon = True
   pdf_service_thread = (
      Thread(target = start_pdf_conversion, args = (pdf, path_for_input_pdf_slides, path_for_jpg_slides,)))
   pdf_service_thread.daemon = True

   video_download_thread.start()
   video_server_thread.start()
   pdf_service_thread.start()

   return 'Success', HTTP_200_OK