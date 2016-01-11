from collections import Counter

class Boolean_search:

	def __init__(self, reverse_index, p_norm = 2):
		self.reverse_index = reverse_index
		self.p_norm = p_norm

	def do_search(self, query, fnc_form = True):
		query = query.lower()

		if(fnc_form):
			search_results = []
			and_clauses = self.split_fnc_query_or(query)

			for and_query in and_clauses:
				x = self.search_and_terms(and_query)
				search_results.extend(x)

			ordered_results = Counter(search_results).most_common() # Order the document by the number of clauses they satisfy, decreasing order.
			print ordered_results
			results = [document_id for (document_id, frequency) in ordered_results]
			return results

		else:
			pass


	def split_fnc_query_or(self, query):
		return query.split('or')


	def search_and_terms(self, query_words):
		relevant_documents = []
		query_words_list = query_words.split('and') # Sets are slow

		first_item = query_words_list[0]
		documents_with_first_word = self.reverse_index[first_item] # Documents AND score per document

		relevant_documents = [document_id for (document_id, frequency) in enumerate(relevant_documents) and document_id in documents_with_word] # We need to initialize with the first item in order to make intersection

		for word in query_words_list[1:]:
			documents_with_word = self.reverse_index[word]
			for (document_id, frequency) in relevant_documents and document_id in documents_with_word:
				relevant_documents.append(document_id)
				print document_id
			# relevant_documents = [document_id for (document_id, frequency) in relevant_documents and document_id in documents_with_word]

		print 'a', relevant_documents
		return relevant_documents

