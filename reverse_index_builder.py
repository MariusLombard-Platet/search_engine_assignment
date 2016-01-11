from collections import Counter, defaultdict
from math import log
from reverse_index import Reverse_index

class Reverse_index_builder:

	PONDERATION_TF_IDF = 'tf_idf'
	PONDERATION_NORMAL_TF_IDF = 'normal_tf_idf'
	PONDERATION_NORMAL_FREQUENCY = 'normal_frequency'

	# Contains, after init, the method that will be called in order to construct the reverse index
	ponderation_method = lambda index: None

	def __init__(self, ponderation_method):
		if(ponderation_method == self.PONDERATION_TF_IDF):
			self.ponderation_method = self.create_with_ponderation_tf_idf

		elif(ponderation_method == self.PONDERATION_NORMAL_TF_IDF):
			self.ponderation_method = self.create_with_ponderation_normal_tf_idf

		elif(ponderation_method == self.PONDERATION_NORMAL_FREQUENCY):
			self.ponderation_method = self.create_with_ponderation_normal_frequency

		else:
			raise Error(ponderation_method)

		return None
 

	def create_reverse_index(self, index):
		return self.ponderation_method(index)

	def create_with_ponderation_tf_idf(self, index):
		N = len(index)
		idf_counter = self.create_idf_counter(index)
		reverse_index = Reverse_index()

		for (i,(document_id, tf_counter)) in enumerate(index):
			for term in tf_counter:
				tf_idf_ponderation = (1 + self.custom_log(tf_counter[term])) * log(float(N) / idf_counter[term])
				reverse_index.add_entry(term, document_id, tf_idf_ponderation)

		return reverse_index


	def create_with_ponderation_normal_tf_idf(self, index):
		# TODO
		pass

	def create_create_with_ponderation_normal_frequency(self, index):
		# TODO
		pass

	def custom_log(self, number, base = 10):
		if number > 0: return log(float(number))
		else: return 0

	def create_idf_counter(self, index):
		idf_counter = defaultdict(int)
		for (document_id, tf_counter) in index:
			for word in tf_counter:
				idf_counter[word] += 1

		# Horribly slow
		# idf_counter = Counter()
		# for (document_id, tf_counter) in index:
		# 	# Increment the idf counter by 1 for each different term contained in tf_counter
		# 	# set(tf_counter) deletes the info about the occurrences, then we simply add with counters
		# 	idf_counter += Counter(set(tf_counter))

		return idf_counter