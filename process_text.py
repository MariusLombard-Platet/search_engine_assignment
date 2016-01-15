import re
from collections import Counter


class Process_text:

    def __init__(self, stop_list_filename):
        self.stop_list = map(str.rstrip, open(stop_list_filename, 'r').readlines())  # Removing \n at the end of each word

    def tokenize(self, text):
        return re.findall('\w+', text)

    def remove_common_words(self, words_list):
        # return [word for word in words_list if word not in self.stop_list]

        # From https://gist.github.com/glenbot/4684356
        # 2x as fast... But it's not a one-liner.
        stop_words = set(self.stop_list)
        for sw in stop_words.intersection(words_list):
            occurences = words_list.count(sw)
            for i in xrange(occurences):
                words_list.remove(sw)

        return words_list

    def word_statistics(self, words_list):
        # This is not normalized by the size of the words. Should it ?
        return Counter(words_list)

    def sanitize_rawtext(self, raw_text):
        # One-liners FTW
        return self.word_statistics(self.remove_common_words(self.tokenize(raw_text.lower())))
