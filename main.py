#!/usr/bin/env python

import Youtube as yt
import YoutubeLivePlaylist as ylp
import os
import sys
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

   while(True):
      try:
         updated_list, live_stream_chunk_urls = playlist.get_current_playlist_urls(live_stream_url)

         if(updated_list):
            for chunk_url in live_stream_chunk_urls:
               video_name_with_path = video_output_path + '/' + str(video_number)
               youtube.download_video_chunk_as_mp4(video_name_with_path, chunk_url)
               video_number = video_number + 1
         else:
            time.sleep(2.5)
            print("Waiting for updated list...")
      except:
         pass

def main(cmd_args):
   if('help' in cmd_args[1] or cmd_args[1] == '-h'):
      print "First arguments is the youtube video URL, second argument the video size e.g. 640x360"
   
   if(len(cmd_args) < 3):
      print "Must provide youtube video URL and video size"
      return
   
   download_video_chunks(cmd_args)

if __name__ == '__main__':
   youtube = yt.Youtube()
   playlist = ylp.YoutubeLivePlaylist()
   try: 
      main(sys.argv)
   except:
      pass