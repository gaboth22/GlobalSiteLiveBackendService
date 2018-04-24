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
      In general, available formats are:
      '91 - 256x144'
      '92 - 426x240'
      '93 - 640x360'
      '94 - 854x480'
      '95 - 1280x720'
      '96 - 1920x1080'
   '''
   def get_live_stream_playlist_url_by_format(self, url, format):
      with youtube_dl.YoutubeDL({}) as ydl:
         available_videos = ydl.extract_info(url, download=False)
         video_format_info = available_videos.get('formats')

         for video_info in video_format_info:
            video_format = self.unicode_string_to_ascii(video_info.get('format'))
            if(format in video_format):
               return self.unicode_string_to_ascii(video_info.get('url'))

      return None

   def download_video_chunk_as_mp4(self, video_name, url):

      if('.mp4' not in video_name):
         video_name = video_name + '.mp4'

      original_filename = video_name.replace('.mp4', '.ts')
      urllib.urlretrieve(url, filename = original_filename)

      while not os.path.isfile(original_filename):
         pass

      #Android
      ff = FFmpeg(
         inputs  = {original_filename : None},
         outputs = {video_name : ['-an', '-s', '640x360', '-vcodec', 'libx264', '-preset', 'fast', '-r', '30', '-x264opts', 'frame-packing=3']}
      )
      print "ffmpeg command:"
      print ff.cmd
      ff.run()

      while not os.path.isfile(video_name):
         pass

      os.remove(original_filename)