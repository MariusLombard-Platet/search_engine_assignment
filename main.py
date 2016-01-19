# coding:utf-8
from parse_docs import Parse_cacm
from reverse_index_builder import Reverse_index_builder
from boolean_search import Boolean_search
from vectorial_search import Vectorial_search
from process_query import Process_query
# import dill
import re
from collections import defaultdict
import configparser
from pprint import pprint


class Search_engine:
    def __init__(self):
        file_config = configparser.ConfigParser()
        file_config.read('config.ini')
        self.config = self._get_real_settings(file_config)

        # TODO: should not parse input file every time.
        Parser = Parse_cacm('sources/cacm.all', 'sources/common_words')
        index = Parser.parse_file()
        reverse_index_builder = Reverse_index_builder(
            ponderation_method=self.config['Reverse_index']['ponderation'],
            index_type=self.config['Reverse_index']['index_type'],
            save_folder_path=self.config['Reverse_index']['save_folder_path']
        )
        self.reverse_index = reverse_index_builder.create_reverse_index(index)

        self._lauch_engine()

    def _lauch_engine(self):
        # Create boolean or vectorial search engine
        if self.config['Research_engine']['type'] == 'vectorial':
            research_engine = Vectorial_search(
                reverse_index=self.reverse_index,
                similarity=self.config['Vectorial_search']['similarity'],
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
            pprint(research_engine.do_search(query_processor.format_query(query)))

    def _get_real_settings(self, user_settings):
        # Checking that all parameters are indeed correct.
        # I'm loving it.
        def _check(first_level, parameter, defaultvalue, expected_type=str, minvalue=None, maxvalue=None, list_of_possible_values=None):
            real_config[first_level][parameter] = self._verify_parameter(
                self._byteify(user_settings[first_level][parameter]),
                defaultvalue,
                expected_type,
                minvalue,
                maxvalue,
                list_of_possible_values
            )

        real_config = defaultdict(dict)

        _check('Boolean_search', 'p_norm', 2., float, 1)
        _check('Boolean_search', 'default_similarity', 0.5, float, 0, 1)
        _check('Vectorial_search', 'similarity', Vectorial_search.SIMILARITY_COSINE, list_of_possible_values=Vectorial_search.SIMILARITY_MODEL_LIST)
        _check('Reverse_index', 'index_type', 'dict', list_of_possible_values=['dict', 'BTree'])
        _check('Reverse_index', 'save_folder_path', 'data/')
        _check('Reverse_index', 'ponderation', Reverse_index_builder.PONDERATION_TF_IDF, list_of_possible_values=Reverse_index_builder.PONDERATION_LIST)
        _check('Research_engine', 'max_results_number', -1, int, minvalue=-1)
        _check('Research_engine', 'type', 'vectorial', list_of_possible_values=['boolean', 'vectorial'])

        return real_config

    def _verify_parameter(self, parameter, defaultvalue, expected_type=str, minvalue=None, maxvalue=None, list_of_possible_values=None):
        # Custom check for integer and float. Yay.
        if expected_type != str:
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

a = Search_engine()
