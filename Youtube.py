#!/usr/bin/env python

from __future__ import unicode_literals
import youtube_dl
import unicodedata
import urllib
import os.path
from ffmpy import FFmpeg

class Youtube:

   def unicode_string_to_ascii(self, unicode_string):
      return unicodedata.normalize('NFKD', unicode_string).encode('ascii','ignore')

   '''
      In general, available sizes are:
      '256x144'
      '426x240'
      '640x360'
      '854x480'
      '1280x720'
      '1920x1080'
   '''
   def get_live_stream_playlist_url_by_size(self, url, size):
      with youtube_dl.YoutubeDL({}) as ydl:
         available_videos = ydl.extract_info(url, download=False)
         video_format_info = available_videos.get('formats')

         for video_info in video_format_info:
            video_format = self.unicode_string_to_ascii(video_info.get('format'))
            if(size in video_format):
               return self.unicode_string_to_ascii(video_info.get('url'))

      return None

   def download_video_chunk_as_mp4(self, video_name, url):

      if('.mp4' not in video_name):
         video_name = video_name + '.mp4'

      original_filename = video_name.replace('.mp4', '.ts')
      urllib.urlretrieve(url, filename = original_filename)

      while not os.path.isfile(original_filename):
         pass

      ff = FFmpeg(
         inputs  = {original_filename : None},
         outputs = {video_name : ['-an', '-vcodec', 'libx264', '-preset', 'ultrafast', '-r', '20']} 
      )
      print "ffmpeg command:"
      print ff.cmd
      ff.run()

      while not os.path.isfile(video_name):
         pass

      os.remove(original_filename)
