#!/usr/bin/env python

import Youtube as yt
import YoutubeLivePlaylist as ylp
import os
import sys
import signal
import shutil
import time
from threading import Thread
from threading import Event

def download_video_chunks(args):
   youtube_link = args[1]
   desired_format = args[2]
   live_stream_url = youtube.get_live_stream_playlist_url_by_format(youtube_link, desired_format)
   video_output_path = 'video'

   if(os.path.exists(video_output_path)):
      shutil.rmtree(video_output_path)
   
   os.makedirs(video_output_path)
   video_number = 0

   while(not kill_event.is_set()):
      updated_list, live_stream_chunk_urls = playlist.get_current_playlist_urls(live_stream_url)

      if(updated_list):
         for chunk_url in live_stream_chunk_urls:
            video_name_with_path = video_output_path + '/' + str(video_number)
            youtube.download_video_chunk_as_mp4(video_name_with_path, chunk_url)
            video_number = video_number + 1
      else:
         time.sleep(2.5)
         print("Waiting for updated list...")

def main(cmd_args):
   if('help' in cmd_args[1] or cmd_args[1] == '-h'):
      print "First arguments is the youtube video URL including https://, second argument the video format e.g. 93"
      print    """ In general, available formats are:
                  '91 - 256x144'
                  '92 - 426x240'
                  '93 - 640x360'
                  '94 - 854x480'
                  '95 - 1280x720'
                  '96 - 1920x1080'"""
   
   if(len(cmd_args) < 3):
      print "Must provide youtube video URL and video format. Pass help or -h for help."
      return

   video_download_thread = Thread(target = download_video_chunks, args = (cmd_args, ))
   video_download_thread.start()
   video_download_thread.join()

def exit_program(signum, frame):
   signal.signal(signal.SIGINT, original_sigint)
   server.close()
   kill_event.set()
   shutil.rmtree('video')
   sys.exit(0)

if __name__ == '__main__':
   kill_event = Event()
   youtube = yt.Youtube()
   playlist = ylp.YoutubeLivePlaylist()
   original_sigint = signal.getsignal(signal.SIGINT)
   signal.signal(signal.SIGINT, exit_program) 
   try: 
      main(sys.argv)
   except:
      pass