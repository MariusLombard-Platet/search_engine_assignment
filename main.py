# coding:utf-8
from reverse_index_builder import Reverse_index_builder
from boolean_search import Boolean_search
from vectorial_search import Vectorial_search
from probabilistic_search import Probabilistic_search
from process_query import Process_query
from config_loader import Config_loader

import time


class Search_engine:
    def __init__(self):
        config_loader = Config_loader('config.ini')
        self.config = config_loader.load_config()

        reverse_index_builder = Reverse_index_builder(
            ponderation_method=self.config['Reverse_index']['ponderation'],
            index_type=self.config['Reverse_index']['index_type'],
            save_folder_path=self.config['Reverse_index']['save_folder_path']
        )
        self.reverse_index = reverse_index_builder.create_reverse_index('sources/cacm.all', 'sources/common_words')

        self._lauch_engine()

    def _lauch_engine(self):
        # Create boolean or vectorial search engine
        if self.config['Research_engine']['type'] == 'vectorial':
            research_engine = Vectorial_search(
                reverse_index=self.reverse_index,
                similarity=self.config['Vectorial_search']['similarity'],
            )
            query_processor = Process_query('sources/common_words', 'vectorial')

        elif self.config['Research_engine']['type'] == 'boolean':
            research_engine = Boolean_search(
                reverse_index=self.reverse_index,
                p_norm=self.config['Boolean_search']['p_norm'],
                default_similarity=self.config['Boolean_search']['default_similarity']
            )
            query_processor = Process_query('sources/common_words', 'boolean')

        elif self.config['Research_engine']['type'] == 'probabilistic':
            research_engine = Probabilistic_search(
                reverse_index=self.reverse_index,
                rsv_relevant_method=self.config['Probabilistic_search']['rsv_relevant_method']
            )

            query_processor = Process_query('sources/common_words', 'probabilistic')
        else:
            raise ValueError('Unsupported research engine type!')

        max_results_number = self.config['Research_engine']['max_results_number']
        while 1:
            query = raw_input('Enter your query: ')
            t0 = time.time()
            results = research_engine.do_search(query_processor.format_query(query))
            print len(results), 'results in', time.time()-t0, 'seconds'
            if max_results_number > 0 and len(results) > max_results_number:
                results = results[:max_results_number]
                print 'printing only the first', max_results_number, 'results: \n'

            print 'document id \t score'
            print '-----------------------------'
            for (document_id, score) in results:
                print document_id, '\t\t', score

a = Search_engine()
