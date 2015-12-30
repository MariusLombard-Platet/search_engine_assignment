import re
from collections import Counter

class Process_text:

	def __init__(self, stop_list_path):
		self.stop_list = map(str.rstrip, open(stop_list_path, 'r').readlines()) # Removing \n at the end of each word

	def tokenize(self, text):
		return re.findall('[\w]+', text)

	def remove_common_words(self, words_list): # Shamelessy stolen from https://gist.github.com/glenbot/4684356
		stop_words = set(self.stop_list)
		for sw in stop_words.intersection(words_list):
		    while sw in words_list:
		        words_list.remove(sw)

		return words_list

	def word_statistics(self, words_list):
		stats = {}
		for word in words_list:
			if(stats.has_key(word)):
				stats[word] += 1
			else:
				stats[word] = 1

		return stats

	def sanitize_rawtext(self, raw_text):
		# One-liner FTW
		return self.word_statistics(self.remove_common_words(self.tokenize(raw_text.lower())))
