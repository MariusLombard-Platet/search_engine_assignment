from collections import defaultdict
from math import log
from reverse_index import Reverse_index
import os.path
import dill


class Reverse_index_builder:

    PONDERATION_TF_IDF = 'tf_idf'
    PONDERATION_NORMAL_TF_IDF = 'normal_tf_idf'
    PONDERATION_NORMAL_FREQUENCY = 'normal_frequency'
    PONDERATION_LIST = [PONDERATION_NORMAL_TF_IDF, PONDERATION_TF_IDF, PONDERATION_NORMAL_FREQUENCY]

    def __init__(self, ponderation_method=PONDERATION_NORMAL_TF_IDF, index_type='dict', save_folder_path='data/'):
        self.save_folder_path = save_folder_path
        self.ponderation_name = ponderation_method
        self.index_type = index_type

        if(ponderation_method == self.PONDERATION_TF_IDF):
            self.ponderation_method = self.create_with_ponderation_tf_idf

        elif(ponderation_method == self.PONDERATION_NORMAL_TF_IDF):
            self.ponderation_method = self.create_with_ponderation_normal_tf_idf

        elif(ponderation_method == self.PONDERATION_NORMAL_FREQUENCY):
            self.ponderation_method = self.create_with_ponderation_normal_frequency

        else:
            raise ValueError(ponderation_method)

        return None

    def create_reverse_index(self, index):
        # Load reverse index if already exists, create it (and save it) otherwise.
        reverse_index_file = self.save_folder_path + self.ponderation_name + '.rev'
        if os.path.isfile(reverse_index_file):
            with open(reverse_index_file, 'rb') as in_strm:
                reverse_index = dill.load(in_strm)
        else:
            reverse_index = self.ponderation_method(index)
            with open(reverse_index_file, 'wb') as output:
                dill.dump(reverse_index, output, dill.HIGHEST_PROTOCOL)

        return reverse_index

    def create_with_ponderation_tf_idf(self, index, compute_norm=True):
        N = len(index)
        reverse_index = Reverse_index(self.index_type)
        reverse_index.idf = self.create_idf_counter(index)
        reverse_index.other_infos['norms'] = defaultdict(lambda: defaultdict(float))
        id_full_list = []

        for (document_id, tf_counter) in index:
            for term in tf_counter:
                tf_idf_ponderation = (1 + self.custom_log(tf_counter[term])) * log(float(N) / reverse_index.idf[term])
                reverse_index.add_entry(term, document_id, tf_idf_ponderation)

                id_full_list.append(document_id)
                if compute_norm:
                    reverse_index.other_infos['norms'][document_id]['linear'] += tf_idf_ponderation
                    reverse_index.other_infos['norms'][document_id]['quadratic'] += tf_idf_ponderation * tf_idf_ponderation

        reverse_index.set_id_set(set(id_full_list))
        reverse_index.other_infos['number of documents'] = N
        reverse_index.other_infos['ponderation_method'] = self.ponderation_name

        return reverse_index

    def create_with_ponderation_normal_tf_idf(self, index):
        reverse_index = self.create_with_ponderation_tf_idf(index, compute_norm=False)
        # We need the unnormalized ponderation for vectorial search, when we normalize the query
        reverse_index.other_infos['max_unnormalized_ponderation'] = defaultdict(float)
        max_ponderation = {}
        N = len(index)

        for word in reverse_index.get_index():
            max_ponderation[word] = max(reverse_index.get_entry(word).values())
            reverse_index.other_infos['max_unnormalized_ponderation'][word] = max_ponderation[word]

            # In-place modification. Avoids huge entries duplications.
            for document_id in reverse_index.get_entry(word):
                reverse_index.get_entry(word)[document_id] = reverse_index.get_entry(word)[document_id] / float(max_ponderation[word])

        # Set norm.
        for (document_id, tf_counter) in index:
            for term in tf_counter:
                sum_element = (1 + self.custom_log(tf_counter[term])) * log(float(N) / reverse_index.idf[term]) / float(max_ponderation[term])
                reverse_index.other_infos['norms'][document_id]['linear'] += sum_element
                reverse_index.other_infos['norms'][document_id]['quadratic'] += sum_element * sum_element

        reverse_index.other_infos['ponderation_method'] = self.ponderation_name

        return reverse_index

    def create_with_ponderation_normal_frequency(self, index):
        # w = tf / max_document (tf)
        N = len(index)
        reverse_index = Reverse_index(self.index_type)
        reverse_index.idf = self.create_idf_counter(index)
        reverse_index.other_infos['norms'] = defaultdict(lambda: defaultdict(float))
        id_full_list = []
        max_frequency_in_document = defaultdict(int)

        # First, create unnormalized reverse index...
        for (document_id, tf_counter) in index:
            for term in tf_counter:
                tf_ponderation = tf_counter[term]
                reverse_index.add_entry(term, document_id, tf_ponderation)
                max_frequency_in_document[document_id] = max(max_frequency_in_document[document_id], tf_ponderation)

                id_full_list.append(document_id)

        # Then, normalize each term by the maximum frequency occurence in the document
        for word in reverse_index.get_all_words():
            for document_id in reverse_index.get_entry(word):
                reverse_index.get_entry(word)[document_id] = reverse_index.get_entry(word)[document_id] / float(max_frequency_in_document[document_id])
                reverse_index.other_infos['norms'][document_id]['linear'] += tf_ponderation
                reverse_index.other_infos['norms'][document_id]['quadratic'] += tf_ponderation * tf_ponderation

        reverse_index.set_id_set(set(id_full_list))
        reverse_index.other_infos['number of documents'] = N
        reverse_index.other_infos['ponderation_method'] = self.ponderation_name

        return reverse_index

    def custom_log(self, number, base=10):
        if number > 0:
            return log(float(number))
        else:
            return 0

    def create_idf_counter(self, index):
        idf_counter = defaultdict(int)
        for (document_id, tf_counter) in index:
            for word in tf_counter:
                idf_counter[word] += 1

        # Horribly slow
        # idf_counter = Counter()
        # for (document_id, tf_counter) in index:
        #   # Increment the idf counter by 1 for each different term contained in tf_counter
        #   # set(tf_counter) deletes the info about the occurrences, then we simply add with counters
        #   idf_counter += Counter(set(tf_counter))

        return idf_counter
