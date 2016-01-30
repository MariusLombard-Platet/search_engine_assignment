import re
from collections import Counter
from stemming import PorterStemmer


class Process_text:

    def __init__(self, stop_list_filename):
        self.stop_list = map(str.rstrip, open(stop_list_filename, 'r').readlines())  # Removing \n at the end of each word
        self.stemmer = PorterStemmer()

    def _tokenize(self, text):
        return re.findall('\w+', text)

    def _stem(self, words_list):
        return map(lambda x: self.stemmer.stem(x, 0, len(x) - 1), words_list)

    def _remove_common_words(self, words_list):
        # return [word for word in words_list if word not in self.stop_list]

        # From https://gist.github.com/glenbot/4684356
        # 2x as fast... But it's not a one-liner.
        stop_words = set(self.stop_list)
        for sw in stop_words.intersection(words_list):
            occurences = words_list.count(sw)
            for i in xrange(occurences):
                words_list.remove(sw)

        return words_list

    def _word_statistics(self, words_list):
        return Counter(words_list)

    def sanitize_rawtext(self, raw_text):
        # Stemming is quite slow, so we remove identified common words, we stem and we remove the common words we did not identify at first.
        # This gives a 15% speedup.
        return self._stem(self._remove_common_words(self._tokenize(raw_text.lower())))

    def sanitize_rawtext_with_stats(self, raw_text):
        # One-liners FTW
        return self._word_statistics(self.sanitize_rawtext(raw_text))
