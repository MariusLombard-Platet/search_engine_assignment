from collections import defaultdict
import operator
from math import log10


class Probabilistic_search:

    PROBABILITY_CONSTANT = 'constant'

    PROBABILITY_LIST = [PROBABILITY_CONSTANT]

    def __init__(self, reverse_index, rsv_relevant_method=PROBABILITY_CONSTANT):
        if rsv_relevant_method not in self.PROBABILITY_LIST:
            raise ValueError(rsv_relevant_method + 'not allowed')

        self.reverse_index = reverse_index
        self.rsv_relevant_method = rsv_relevant_method

        self._add_relevant_contribution = getattr(self, '_add_relevant_contribution_' + self.rsv_relevant_method)

    def do_search(self, query):
        rsv_results = defaultdict(float)  # Format : {relevant_document_id: rsv_value}
        for word in query:
            relevant_documents = self.reverse_index.get_ids_for_term(word)
            for relevant_document_id in relevant_documents:
                rsv_results[relevant_document_id] += self._add_relevant_contribution() + self._add_nonrelevant_contribution(word)

        return sorted(rsv_results.items(), key=operator.itemgetter(1), reverse=True)

    def _add_relevant_contribution_constant(self):
        return 0

    def _add_nonrelevant_contribution(self, word):
        return log10(self.reverse_index.other_infos['number_of_documents'] / float(len(self.reverse_index.get_entry(word))))
