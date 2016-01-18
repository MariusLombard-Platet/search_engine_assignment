from BTrees.OOBTree import OOBTree
from collections import defaultdict


class Reverse_index:
    def __init__(self, index_type='dict'):  # BTrees are slow
        if index_type == 'BTree':
            self.reverse_index = OOBTree()
            self.index_type = 'BTree'
        elif index_type == 'dict':
            self.reverse_index = defaultdict(dict)
            self.index_type = 'defaultdict'
        else:
            raise ValueError('Incorrect index type!')

        self.id_set = None
        self.idf = {}
        self.other_infos = {}

        return None

    def _store_all_ids(self):
        ids_list = []
        for word in self.reverse_index:
            ids_list.extend(self.reverse_index[word].keys())

        return set(ids_list)

    def get_index(self):
        return self.reverse_index

    def get_entry(self, term):
        return self.reverse_index[term]

    def get_all_ids_set(self):
        if self.id_set:
            return self.id_set
        else:
            self.set_id_set(self._store_all_ids())
            return self.id_set

    def set_id_set(self, id_set):
        self.id_set = id_set
        return None

    def get_ids_for_term(self, term):
        return self.get_entry(term).keys()

    def get_ponderation(self, term, document_id):
        dict_of_docs = self.get_entry(term)

        if document_id in dict_of_docs.keys():
            return dict_of_docs[document_id]
        else:
            return 0

    def get_all_words(self):
        return self.get_index().keys()

    def add_entry(self, term, document_id, ponderation):
        if self.index_type == 'BTree':
            self._add_entry_btree(term, document_id, ponderation)
        else:
            self._add_entry_defaultdict(term, document_id, ponderation)

        return None

    def _add_entry_defaultdict(self, term, document_id, ponderation):
        self.reverse_index[term][document_id] = ponderation

        return None

    def _add_entry_btree(self, term, document_id, ponderation):
        if(term in self.reverse_index.keys()):  # The term is already in the tree
            self.reverse_index[term][document_id] = ponderation
        else:
            self.reverse_index[term] = {document_id: ponderation}

        return None
