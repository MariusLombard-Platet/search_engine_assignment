from collections import Counter, defaultdict
from reverse_index_builder import Reverse_index_builder
from math import log
import operator


class Vectorial_search:

    SIMILARITY_COSINE = 'cosine'
    SIMILARITY_DICE = 'dice'
    SIMILARITY_JACCARD = 'jaccard'
    SIMILARITY_OVERLAP = 'overlap'
    SIMILARITY_MODEL_LIST = [SIMILARITY_COSINE, SIMILARITY_DICE, SIMILARITY_JACCARD, SIMILARITY_OVERLAP]

    def __init__(self,
                 reverse_index,
                 similarity=SIMILARITY_COSINE,
                 ponderation=Reverse_index_builder.PONDERATION_NORMAL_TF_IDF,
                 max_results_number=15
                 ):

        # Double dependancy (index_builder and this) to ponderation method. Urgh.
        similarity = similarity.lower()
        if similarity not in self.SIMILARITY_MODEL_LIST:
            raise ValueError(similarity)
        else:
            self.reverse_index = reverse_index
            self.searching_method = getattr(self, '_search_' + similarity)

        self.ponderation = ponderation
        self.max_results_number = max_results_number

    def do_search(self, query):
        query_words = query.split()
        similarities = self.searching_method(query_words)
        return [
            document_id for (document_id, similarity) in
            sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)[:self.max_results_number]
        ]

    def _search_cosine(self, query_words):
        document_similarities = {}
        query_weights = self._query_weight(query_words, self.reverse_index.idf)
        documents_norm = defaultdict(float)  # Contains the sum of the squares of the ponderation for every word, for every document

        # Multiply ponderations from document and from query
        documents_unnormalized_similarities = defaultdict(float)
        for word in self.reverse_index.get_all_words():
            for document_id in self.reverse_index.get_ids_for_term(word):
                ponderation = self.reverse_index.get_ponderation(word, document_id)
                documents_unnormalized_similarities[document_id] += ponderation * query_weights[word]
                documents_norm[document_id] += ponderation ** 2

        # Then, divide each document by the sum of the square of its weights
        for document_id in documents_unnormalized_similarities:
            document_similarities[document_id] = documents_unnormalized_similarities[document_id] / float(documents_norm[document_id])
        # We don't need to divide by the norm of the query vector, since it is the same for every document.

        # Order by similarities, return document_ids
        return document_similarities

    def _search_dice(self, query_words):
        pass

    def _search_jaccard(self, query_words):
        pass

    def _search_overlap(self, query_words):
        pass

    def _query_weight(self, query_words, idf_counter):
        tf_counter = Counter(query_words)

        # We assume that the corpus is so large that the bag of words of the query won't significantly change the idf count
        # Or, in other words, that we don't care about it.
        # See http://nlp.stanford.edu/IR-book/html/htmledition/queries-as-vectors-1.html
        if self.ponderation == Reverse_index_builder.PONDERATION_TF_IDF:
            query_weights = self._query_weight_tf_idf(query_words, idf_counter, tf_counter)

        elif self.ponderation == Reverse_index_builder.PONDERATION_NORMAL_TF_IDF:
            query_weights_unnormalized = self._query_weight_tf_idf(query_words, idf_counter, tf_counter)
            query_weights = defaultdict(float)

            for word in query_weights_unnormalized:
                query_weights[word] = query_weights_unnormalized[word] / self.reverse_index.other_infos['max_unnormalized_ponderation'][word]

        elif self.ponderation == Reverse_index_builder.PONDERATION_NORMAL_FREQUENCY:
            pass

        return query_weights

    def _query_weight_tf_idf(self, query_words, idf_counter, tf_counter):
        query_weights = defaultdict(float)
        N = self.reverse_index.other_infos['number of documents']
        for word in query_words:
            query_weights[word] = (1 + self._custom_log(tf_counter[word])) * log(float(N) / idf_counter[word])

        return query_weights

    def _custom_log(self, number, base=10):
        if number > 0:
            return log(float(number))
        else:
            return 0
