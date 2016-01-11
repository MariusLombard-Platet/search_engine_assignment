from BTrees.OOBTree import OOBTree
from collections import defaultdict

class Reverse_index:
	def __init__(self, index_type = 'dict'): # BTrees are slow
		if index_type == 'BTree':
			self.reverse_index = OOBTree()
			self.index_type = 'BTree'
		else:
			self.reverse_index = defaultdict(list)
			self.index_type = 'defaultdict'

		return None


	def get_index(self):
		return self.reverse_index

	def get(self, term):
		return self.reverse_index[term]

	def add_entry(self, term, document_id, ponderation):
		if self.index_type == 'BTree':
			self.add_entry_btree(term, document_id, ponderation)
		else:
			self.add_entry_defaultdict(term, document_id, ponderation)

		return None


	def add_entry_defaultdict(self, term, document_id, ponderation):
		self.reverse_index[term].append((document_id, ponderation))
		
		return None


	def add_entry_btree(self, term, document_id, ponderation):
		if(term in self.reverse_index.keys()): # the term is already in the tree
			self.reverse_index[term].append((document_id, ponderation))
		else:
			self.reverse_index[term] = [(document_id, ponderation)]

		return None

