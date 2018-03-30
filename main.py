#!/usr/bin/env python

import Youtube as yt
import YoutubeLivePlaylistParser as ylpp

def main():
	parser = ylpp.YoutubeLivePlaylistParser()
	youtube = yt.Youtube()

	youtube_link = 'https://www.youtube.com/watch?v=3yzvwwl3oyI'
	desired_size = '640x360'
	live_stream_url = youtube.get_live_stream_playlist_url_by_size(youtube_link, desired_size)
	video_number = 0

	while(True):
		updated_list, live_stream_chunk_urls = parser.get_current_playlist_urls(live_stream_url)

		if(updated_list):
			for chunk_url in live_stream_chunk_urls:
				youtube.download_video_chunk_as_mp4(str(video_number), chunk_url)
				video_number = video_number + 1
		else:
			print("Waiting for updated list...")

if __name__ == '__main__':
	main()