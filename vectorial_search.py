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
                 max_results_number=-1
                 ):

        similarity = similarity.lower()
        if similarity not in self.SIMILARITY_MODEL_LIST:
            raise ValueError(similarity)
        else:
            self.reverse_index = reverse_index
            self.similarity_method = similarity

        self.ponderation = self.reverse_index.other_infos['ponderation_method']
        self.max_results_number = max_results_number

    def do_search(self, query):
        """
        Vectorial search on a query that has been processed by Process_query.
        """
        # Only search on words that are actually in the corpus
        significant_query_words = list(set(query).intersection(set(self.reverse_index.get_all_words())))

        # Do the search
        similarities = self._search(significant_query_words)

        # Removing documents with similarity of 0
        positive_similarities = {}
        for document_id, similarity in similarities.iteritems():
            if similarity > 0:
                positive_similarities[document_id] = similarity

        # Rank and truncate
        ranked_similarities = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
        if self.max_results_number > 0:
            ranked_similarities = ranked_similarities[:self.max_results_number]

        return [document_id for (document_id, similarity) in ranked_similarities]

    def _search(self, query_words):
        document_similarities = {}
        query_weights = self._query_weight(query_words, self.reverse_index.idf)
        query_norms = {
            'linear': sum(query_weights.values()),
            'quadratic': sum(map(lambda x: x*x, query_weights.values()))
        }

        documents_unnormalized_similarities = defaultdict(float)

        # Multiply ponderations from document and from query
        for word in query_words:
            for document_id in self.reverse_index.get_ids_for_term(word):
                ponderation = self.reverse_index.get_ponderation(word, document_id)

                documents_unnormalized_similarities[document_id] += getattr(
                    self, '_get_search_numerator_' + self.similarity_method
                    )(ponderation, query_weights[word])

        # Then, divide each document by the normalizing function for given similarity method
        for document_id in documents_unnormalized_similarities:
            denominator = getattr(self, '_get_normalizing_term_' + self.similarity_method)(
                self.reverse_index.other_infos['norms'][document_id],
                query_norms,
                documents_unnormalized_similarities[document_id]
            )

            document_similarities[document_id] = documents_unnormalized_similarities[document_id] / float(denominator)

        return document_similarities

    def _get_search_numerator_cosine(self, document_word_ponderation, query_weight):
        return document_word_ponderation * query_weight

    def _get_search_numerator_dice(self, document_word_ponderation, query_weight):
        return 2 * document_word_ponderation * query_weight

    def _get_search_numerator_jaccard(self, document_word_ponderation, query_weight):
        return document_word_ponderation * query_weight

    def _get_search_numerator_overlap(self, document_word_ponderation, query_weight):
        return document_word_ponderation * query_weight

    def _get_normalizing_term_cosine(self, document_norms, query_norms, document_unnormalized_similarities):
        return (document_norms['quadratic'] * query_norms['quadratic']) ** 0.5

    def _get_normalizing_term_dice(self, document_norms, query_norms, document_unnormalized_similarities):
        return document_norms['linear'] + query_norms['linear']

    def _get_normalizing_term_jaccard(self, document_norms, query_norms, document_unnormalized_similarities):
        return document_norms['linear'] + query_norms['linear'] - document_unnormalized_similarities

    def _get_normalizing_term_overlap(self, document_norms, query_norms, document_unnormalized_similarities):
        return min(document_norms['linear'], query_norms['linear'])

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
                query_weights[word] = query_weights_unnormalized[word] / float(self.reverse_index.other_infos['max_unnormalized_ponderation'][word])

        elif self.ponderation == Reverse_index_builder.PONDERATION_NORMAL_FREQUENCY:
            query_weights = self._query_weight_normalized_frequency(query_words)

        return query_weights

    def _query_weight_tf_idf(self, query_words, idf_counter, tf_counter):
        query_weights = defaultdict(float)
        N = self.reverse_index.other_infos['number of documents']
        for word in query_words:
            query_weights[word] = (1 + self._custom_log(tf_counter[word])) * log(float(N) / idf_counter[word])

        return query_weights

    def _query_weight_normalized_frequency(self, query_words):
        word_count = Counter(query_words)
        # When the query does not have any significant word.
        if len(word_count) == 0:
            return {}

        maximum_frequency = word_count.most_common(1)[0][1]  # Find the highest frequency in the query
        query_weights = defaultdict(float)
        for word in query_words:
            query_weights[word] = word_count[word] / float(maximum_frequency)

        return query_weights

    def _custom_log(self, number, base=10):
        if number > 0:
            return log(float(number))
        else:
            return 0
