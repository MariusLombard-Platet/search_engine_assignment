from collections import defaultdict
import operator


class Boolean_search:

    def __init__(self, reverse_index, p_norm=2):
        self.reverse_index = reverse_index
        self.p_norm = p_norm
        self.default_similarity = 0.5

    def do_search(self, query):
        """
        The search MUST be in CNF (a AND b AND c OR b AND d OR ...), without parenthesis
        """
        query = query.lower()
        and_clauses = self.split_fnc_query_or(query)

        similarities_for_all_clauses = defaultdict(list)
        for and_query in and_clauses:
            similarities_for_clause = self.search_and_terms(and_query)

            for document_id in similarities_for_clause:
                similarities_for_all_clauses[document_id].append(similarities_for_clause[document_id])

        result_with_similarities = self.similarity_or_query(similarities_for_all_clauses)
        sorted_results = sorted(result_with_similarities.items(), key=operator.itemgetter(1), reverse=True)  # Sort by decreasing similarity

        return map(lambda (document_id, similarity): document_id, sorted_results)  # Only return the document_ids

    def similarity_or_query(self, similarities_for_all_clauses):
        """
        Computes the similarity for every document on a query like "k1 OR k2 OR k3 ..."
        where ki are actually already determined in terms of similarity (which is the case in a NCF query :
        we first compute similarities for all clauses k1 = l1 AND l2 AND l3 AND ..., so there is no problem.)
        """
        result_with_similarities = {}

        for document_id in similarities_for_all_clauses:
            similiarities_for_document = similarities_for_all_clauses[document_id]

            sum_similarities = 0
            for similarity in similiarities_for_document:
                sum_similarities += similarity ** self.p_norm

            result_with_similarities[document_id] = (sum_similarities / float(len(similiarities_for_document))) ** self.p_norm

        return result_with_similarities

    def split_fnc_query_or(self, query):
        return query.split(' or ')

    def search_and_terms(self, query_words):
        query_words_list = query_words.split(' and ')
        relevant_documents_id = self.get_relevant_documents_ids(query_words_list)

        # Extended Boolean Model ranking.
        # See https://en.wikipedia.org/wiki/Extended_Boolean_model
        # Difference is that, we apply this ranking onto a classical boolean retrieval
        # (extended boolean can retrieve docs that do not satisfy all AND clauses, we don't)
        # First, collect the ponderations of the documents that satisfy all AND propositions of the clause
        documents_weights = defaultdict(list)
        for word in query_words_list:
            for document_id in relevant_documents_id:

                ponderation = self.reverse_index.get_ponderation(word, document_id)
                if ponderation is not None:
                    documents_weights[document_id].append(self.reverse_index.get_ponderation(word, document_id))

        similarities = defaultdict(list)

        # Then, compute similarity value based on these ponderations, for every document
        for document_id in documents_weights:
            similarity_sum = 0

            for weight in documents_weights[document_id]:
                similarity_sum += (1 - weight) ** self.p_norm

            similarities[document_id] = 1 - (similarity_sum / float(len(documents_weights[document_id]))) ** (1. / self.p_norm)

        # Some documents can not having any score now, because the NOT do not give any,
        # so typically NOT a AND NOT b will not give any score to the closure.
        # We just re-add these documents with default similarity
        for document_id in relevant_documents_id:
            if document_id not in similarities:
                similarities[document_id] = self.default_similarity

        return similarities

    # Could go faster if we pre-order the words by increasing size of their reverse index
    def get_relevant_documents_ids(self, query_words_list):
        first_word_clause = query_words_list[0]

        relevant_documents_ids = self.find_set_for_word_clause(first_word_clause)
        for unary_word in query_words_list[1:]:
            relevant_documents_ids = relevant_documents_ids.intersection(self.find_set_for_word_clause(unary_word))

        return list(relevant_documents_ids)

    def find_set_for_word_clause(self, unary_word):
        """
        Find set of document ids which contain a word (or do not contain a word)
        """
        if unary_word[:4] == 'not ':  # unary_word is 'word' or 'not word'
            return (self.reverse_index.get_all_ids_set()).difference(set(self.reverse_index.get_ids_for_term(unary_word[4:].strip())))
        else:
            return set(self.reverse_index.get_ids_for_term(unary_word.strip()))
