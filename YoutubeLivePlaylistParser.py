#!/usr/bin/env python

import requests
import unicodedata
import time

class YoutubeLivePlaylistParser:

	def __init__(self):
		self.current_playlist_sequence_end_number = 0

	def unicode_string_to_ascii(self, unicode_string):
		return unicodedata.normalize('NFKD', unicode_string).encode('ascii','ignore')

	'''
		Return a list containing the current playlist urls
	'''
	def get_current_playlist_urls(self, url):
		r = requests.get(url)
		r.encoding = 'utf-8'

		if(r.status_code != 200):
			return (False, None)

		playlist_file = r.text
		target_duration_matcher = '#EXT-X-TARGETDURATION:'
		target_duration_index = (
			playlist_file.find(target_duration_matcher) + 
			len(target_duration_matcher))
		current_index = target_duration_index
		target_duration = ''

		while playlist_file[current_index] != '\n':
			target_duration = target_duration + playlist_file[current_index]
			current_index = current_index + 1

		media_seq_numb_matcher = '#EXT-X-MEDIA-SEQUENCE:'
		sequence_number_index = (
			playlist_file.find(media_seq_numb_matcher) + 
			len(media_seq_numb_matcher))
		current_index = sequence_number_index
		playlist_sequence_start_number = ''

		while playlist_file[current_index] != '\n':
			playlist_sequence_start_number = (
				playlist_sequence_start_number + 
				playlist_file[current_index])
			current_index = current_index + 1

		playlist_sequence_start_number = long(float(playlist_sequence_start_number.strip()))
		url_delimiter = '\n#EXTINF:' + str(target_duration) + '.0,\n'
		playlist_url_list = playlist_file.split(url_delimiter)
		del playlist_url_list[0]
		updated_playlist = False

		if(playlist_sequence_start_number >= self.current_playlist_sequence_end_number):
			updated_playlist = True	
			self.current_playlist_sequence_end_number = (
				playlist_sequence_start_number +
				len(playlist_url_list))

		ascii_list = []
		for chunk_url in playlist_url_list:
			ascii_list.append(self.unicode_string_to_ascii(chunk_url).strip().replace('\n', ''))

		return (updated_playlist, ascii_list[:])