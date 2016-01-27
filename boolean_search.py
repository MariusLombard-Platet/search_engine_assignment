from collections import defaultdict
import operator
from reverse_index_builder import Reverse_index_builder


class Boolean_search:

    def __init__(self, reverse_index, p_norm=2):
        self.reverse_index = reverse_index
        self.p_norm = p_norm
        self.default_similarity = 0.5

        if reverse_index.other_infos['ponderations_method'] != Reverse_index_builder.PONDERATION_NORMAL_TF_IDF:
            raise ValueError('Boolean request cannot be done with such ponderation method. Please change ponderation to a normalized one')

    def do_search(self, query):
        """
        Boolean search on a query that has been processed by Process_query.
        """
        and_clauses_list = query

        similarities_for_all_clauses = defaultdict(list)
        for and_clause in and_clauses_list:
            similarities_for_clause = self._search_and_clauses(and_clause)

            for document_id in similarities_for_clause:
                similarities_for_all_clauses[document_id].append(similarities_for_clause[document_id])

        result_with_similarities = self._similarity_or_query(similarities_for_all_clauses)

        return sorted(result_with_similarities.items(), key=operator.itemgetter(1), reverse=True)  # Sort by decreasing similarity

    def _similarity_or_query(self, similarities_for_all_clauses):
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

    # def split_fnc_query_or(self, query):
    #     return query.split(' or ')

    def _search_and_clauses(self, and_clause_list):
        relevant_documents_id = self._get_relevant_documents_ids(and_clause_list)

        # Extended Boolean Model ranking.
        # See https://en.wikipedia.org/wiki/Extended_Boolean_model
        # Difference is that, we apply this ranking onto a classical boolean retrieval
        # (extended boolean can retrieve docs that do not satisfy all AND clauses, we don't)
        # First, collect the ponderations of the documents that satisfy all AND propositions of the clause
        documents_weights = defaultdict(list)
        for word in and_clause_list:
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

        # Some documents can have no score now, because the NOT do not give any,
        # so typically NOT a AND NOT b will not give any score to the closure.
        # We just re-add these documents with default similarity
        for document_id in relevant_documents_id:
            if document_id not in similarities:
                similarities[document_id] = self.default_similarity

        return similarities

    def _get_relevant_documents_ids(self, and_clause_list):
        # For all words in clause list, get the set of all documents that contain (or do not contain if NOT keyword is present) said word.
        list_of_relevant_documents_id_sets = map(self._find_set_for_word_clause, and_clause_list)

        if len(list_of_relevant_documents_id_sets) == 0:
            return []

        # Order the results by the size of the sets, so the intersection will be faster to compute
        ordered_list_of_relevant_documents_id_sets = sorted(list_of_relevant_documents_id_sets, key=len)

        # Do the intersection
        relevant_documents_ids = ordered_list_of_relevant_documents_id_sets[0]
        for relevant_documents_id_set in ordered_list_of_relevant_documents_id_sets[1:]:
            relevant_documents_ids = relevant_documents_ids.intersection(relevant_documents_id_set)

        return list(relevant_documents_ids)

    def _find_set_for_word_clause(self, unary_word):
        """
        Find set of document ids which contain a word (or do not contain a word)
        """
        if unary_word[:4] == 'not ':  # unary_word is 'word' or 'not word'
            return (self.reverse_index.get_all_ids_set()).difference(set(self.reverse_index.get_ids_for_term(unary_word[4:].strip())))
        else:
            return set(self.reverse_index.get_ids_for_term(unary_word.strip()))
