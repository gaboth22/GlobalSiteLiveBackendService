#!/usr/bin/env python

import Youtube as yt
import YoutubeLivePlaylist as ylp
import os
import shutil
import time

class VideoChunkDownloader:
   def clear_stale_data(self, video_output_path):
      if(os.path.exists(video_output_path)):
         shutil.rmtree(video_output_path)

   def start(self, youtube_link, desired_format, video_output_path):
      youtube = yt.Youtube()
      playlist = ylp.YoutubeLivePlaylist()

      live_stream_url = youtube.get_live_stream_playlist_url_by_format(youtube_link, desired_format)

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
               print("Waiting for updated list...")
               time.sleep(1.5)
         except:
            pass
