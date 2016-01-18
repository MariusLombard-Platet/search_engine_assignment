# coding:utf-8
from parse_docs import Parse_cacm
from reverse_index_builder import Reverse_index_builder
from boolean_search import Boolean_search
from vectorial_search import Vectorial_search
import json
from process_query import Process_query
# import dill
import re
from collections import defaultdict
import configparser


class Search_engine:
    def __init__(self):
        file_config = configparser.ConfigParser()
        file_config.read('config.ini')
        self.config = self._get_real_settings(file_config)

        Parser = Parse_cacm('sources/cacm.all', 'sources/common_words')
        index = Parser.parse_file()
        reverse_index_builder = Reverse_index_builder()
        self.reverse_index = reverse_index_builder.create_reverse_index(index)


        self._lauch_engine()

    def _lauch_engine(self):
        # Create boolean or vectorial search engine
        if self.config['Research_engine']['type'] == 'vectorial':
            research_engine = Vectorial_search(
                reverse_index=self.reverse_index,
                similarity=Vectorial_search.SIMILARITY_COSINE,
                max_results_number=self.config['Research_engine']['max_results_number']
            )
            query_processor = Process_query('sources/common_words', 'vectorial')


        elif self.config['Research_engine']['type'] == 'boolean':
            research_engine = Boolean_search(
                reverse_index=self.reverse_index,
                p_norm=self.config['Boolean_search']['p_norm'],
                max_results_number=self.config['Research_engine']['max_results_number']
            )
            query_processor = Process_query('sources/common_words', 'boolean')

        else:
            raise ValueError('Unsupported research engine type!')

        while 1:
            query = raw_input('Enter your query:')
            print research_engine.do_search(query_processor.format_query(query))


    def _get_real_settings(self, user_settings):

        # Checking that all parameters are indeed correct.
        # I'm loving it.
        def _check(first_level, parameter, defaultvalue, expected_type=None, minvalue=None, maxvalue=None, list_of_possible_values=None):
            real_config[first_level][parameter] = self._verify_parameter(self._byteify(user_settings[first_level][parameter]), defaultvalue, expected_type, minvalue, maxvalue, list_of_possible_values)


        real_config = defaultdict(dict)

        _check('Boolean_search', 'p_norm', 2., float, 1)
        _check('Boolean_search', 'default_similarity', 0.5, float, 0, 1)
        _check('Vectorial_search', 'similarity', Vectorial_search.SIMILARITY_COSINE, list_of_possible_values=Vectorial_search.SIMILARITY_MODEL_LIST)
        _check('Reverse_index', 'index_type', 'dict', list_of_possible_values=['dict', 'BTree'])
        _check('Reverse_index', 'ponderation', Reverse_index_builder.PONDERATION_TF_IDF, list_of_possible_values=Reverse_index_builder.PONDERATION_LIST)
        _check('Research_engine', 'max_results_number', -1, int, minvalue=-1)
        _check('Research_engine', 'type', 'vectorial', list_of_possible_values=['boolean', 'vectorial'])

        return real_config

    def _verify_parameter(self, parameter, defaultvalue, expected_type=None, minvalue=None, maxvalue=None, list_of_possible_values=None):
        # Custom check for integer and float. Yay.
        if expected_type and expected_type != str:
            if expected_type == float:
                if re.match("^\d+?\.\d?$", parameter) is None:
                    return defaultvalue
                else:
                    parameter = float(parameter)

            elif expected_type == int:
                if re.match("^-?\d+$", parameter) is None:
                    return defaultvalue
                else:
                    parameter = int(parameter)

        if minvalue and parameter < minvalue:
            return defaultvalue

        if maxvalue and parameter > maxvalue:
            return defaultvalue

        if list_of_possible_values and parameter not in list_of_possible_values:
            return defaultvalue

        return parameter

    def _byteify(self, input):
        """
        Transforms unicode objects to UTF-8 ones.
        Copied from stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python#answer-13105359
        """
        if isinstance(input, dict):
            return {self._byteify(key): self._byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self._byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

# print 'lol'
a = Search_engine()

# t0 = time.time()
# Parser = Parse_cacm('sources/cacm.all', 'sources/common_words')
# query_processor = Process_query('sources/common_words')

# t1 = time.time()
# print 'parse init : ', t1 - t0

# index = Parser.parse_file()
# t2 = time.time()
# print 'parsing : ', t2 - t1

# Reverse_index_builder = Reverse_index_builder()
# reverse_index = Reverse_index_builder.create_reverse_index(index)

# # with open('full_reverse_index_motherfucka.bck', 'wb') as output:
# #     dill.dump(reverse_index, output, dill.HIGHEST_PROTOCOL)

# t4 = time.time()
# print 'rev_index : ', t4 - t2

# # boolean_search = Boolean_search(reverse_index)
# # # boolean_query = query_processor.create_boolean_query_from_json(json.dumps(
# # #     [['TSS'], ['deal'], ['Time'], ['Sharing'], ['System'], ['operating'], ['system'], ['IBM'], ['computers']]
# # # ))
# # boolean_query = query_processor.create_boolean_query_from_json(json.dumps([['NOT IBM', 'NOT computer'], ['NOT IBM', 'NOT analysis'], ['language']]))


# # print 'dump', boolean_query
# # # print 'results to query "multiplexor OR nonrational OR series AND NOT conclusion" : ',
# # print boolean_search.do_search(boolean_query)

# vectorial_search = Vectorial_search(reverse_index, Vectorial_search.SIMILARITY_COSINE)
# query = query_processor.create_vectorial_query_from_string("""which deal with TSS (Time Sharing System), an
# operating system for IBM computers?""")
# print vectorial_search.do_search(query)

# t6 = time.time()
# print 'search : ', t6 - t4
# print 'total : ', t6 - t0
