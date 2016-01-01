from collections import Counter
from BTrees.OOBTree import OOBTree
from math import log

class reverse_index:

	PONDERATION_TF_IDF = 'tf_idf'
	PONDERATION_NORMAL_TF_IDF = 'normal_tf_idf'
	PONDERATION_NORMAL_FREQUENCY = 'normal_frequency'

	# Contains, after init, the method that will be called in order to construct the reverse index
	ponderation_method = lambda index: None

	def __init__(ponderation_method):
		if(ponderation_method == PONDERATION_TF_IDF):
			self.ponderation_method = self.create_with_ponderation_tf_idf

		elif(ponderation_method == PONDERATION_NORMAL_TF_IDF):
			self.ponderation_method = self.create_with_ponderation_normal_tf_idf

		elif(ponderation_method == PONDERATION_NORMAL_FREQUENCY):
			self.ponderation_method = self.create_with_ponderation_normal_frequency

		else:
			raise Error(ponderation_method)
 

	def create_inverse_index(index):
		return self.ponderation_method(index)

	def create_with_ponderation_tf_idf(index):
		N = index.length()
		idf_counter = self.create_idf_counter(index)

		inverse_index = OOBTree()

		for (document_id, tf_counter) in enumerate(index):
			for (term, tf) in tf_counter:
				tf_idf_ponderation = (1 + self.custom_log(tf)) * log(N / idf_counter[word])

				if(word in inverse_index.keys()): # the term is already in the tree
					inverse_index[word].append((document_id, tf_idf_ponderation))
				else:
					inverse_index[word] = [(document_id, tf_idf_ponderation)]

		return inverse_index


	def create_with_ponderation_normal_tf_idf(index):
		# TODO
		pass

	def create_create_with_ponderation_normal_frequency(index):
		# TODO
		pass

	def custom_log(number, base = 10):
		if number > 0: return math.log(number, base)
		else: return 0

	def create_idf_counter(index):
		idf_counter = Counter()

		for (document_id, tf_counter) in index:
			# Increment the idf counter by 1 for each different term contained in tf_counter
			# set(tf_counter) deletes the info about the occurrences, then we simply add with counters
			idf_counter += Counter(set(tf_counter))

		return idf_counter