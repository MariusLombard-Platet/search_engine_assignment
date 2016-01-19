from collections import defaultdict
from parse_docs import Parse_cacm
from reverse_index_builder import Reverse_index_builder
from vectorial_search import Vectorial_search
# For boolean search, we would have to pre-process the queries, ie, to cheat
from process_query import Process_query
import time


class Measures:
    """
    Quick and dirty code to parse test queries and expected results, and to get measures on code accuracy
    """

    def __init__(
            self,
            queries_filename,
            answers_filename,
            ponderation_method=Reverse_index_builder.PONDERATION_NORMAL_TF_IDF,
            similarity_method=Vectorial_search.SIMILARITY_COSINE
            ):

        # self.query_answer = self._parse_queries_answers(queries_filename, answers_filename)
        self.queries_filename = queries_filename
        self.answers_filename = answers_filename
        self.ponderation_method = ponderation_method
        self.similarity_method = similarity_method
        self.beta = 1
        self.alpha = 1. / (1 + self.beta ** 2)
        self.lines = []

    def run_testing(self):
        print 'Launching tests!'
        print 'Loading database...',
        Parser = Parse_cacm('sources/cacm.all', 'sources/common_words')
        index = Parser.parse_file()
        reverse_index_builder = Reverse_index_builder(self.ponderation_method)
        reverse_index = reverse_index_builder.create_reverse_index(index)
        print ' Done'

        print 'Loading test data...',
        # {query: [answer1, answer2...]}
        self.query_answer = self._parse_queries_answers(self.queries_filename, self.answers_filename)
        print ' Done'

        print 'Initializing variables...',
        time_parsing_queries = 0.
        time_doing_researches = 0.
        precision = []
        recall = []
        r_measure = []
        f_measure = []
        vectorial_search = Vectorial_search(reverse_index, self.similarity_method)
        query_processor = Process_query(stop_list_filename='sources/cacm.all')
        print ' Done'

        t0 = time.time()
        print 'Let\'s get to it! (this may take 5-10 seconds)'
        for query in self.query_answer:
            expected_answers = self.query_answer[query]

            t_init = time.time()
            processed_query = query_processor.format_query(query)
            t_parse = time.time()
            time_parsing_queries += t_parse - t_init

            answers = vectorial_search.do_search(processed_query)
            t_query = time.time()
            time_doing_researches += t_query - t_parse

            precision.append(self._compute_precision(answers, expected_answers))
            recall.append(self._compute_recall(answers, expected_answers))
            r_measure.append(self._compute_r_measure(answers, expected_answers))
            f_measure.append(self._compute_f_measure(precision[-1], recall[-1]))

        number_of_tests = float(len(self.query_answer))
        print 'Number of queries tested:', int(number_of_tests), 'in', round(time.time() - t0, 2), 'seconds'
        print 'Average time spent on query processing:', time_parsing_queries / number_of_tests, 'seconds',
        print ', doing the research:', time_doing_researches / number_of_tests, 'seconds'
        print 'Average time spent on a query (total):', (time_doing_researches + time_parsing_queries) / number_of_tests, 'seconds'
        print """
###################################
#      PERFORMANCE MEASURES       #
###################################"""
        print 'Max Precision:', max(precision), 'average (MAP):', reduce(lambda x, y: x + y, precision) / len(precision)
        print 'Max Recall:', max(recall), 'average:', reduce(lambda x, y: x + y, recall) / len(recall)
        print 'Max F-measure', max(f_measure), 'average:', reduce(lambda x, y: x + y, f_measure) / len(f_measure)
        print 'Min E-measure', 1 - max(f_measure), 'average:', 1 - reduce(lambda x, y: (x + y), f_measure) / len(f_measure)
        print 'Max R-measure', max(r_measure), 'average:', reduce(lambda x, y: x + y, r_measure) / len(r_measure)

    def _compute_precision(self, answers, expected_answers):
        correct_answers_found = set(expected_answers).intersection(answers)
        return len(correct_answers_found) / float(len(answers))

    def _compute_recall(self, answers, expected_answers):
        correct_answers_found = set(expected_answers).intersection(answers)
        # Handle case where there is no expected answer : answer = [] => recall = 1, otherwise 0
        if len(expected_answers) != 0:
            return len(correct_answers_found) / float(len(expected_answers))
        else:
            if len(answers) == 0:
                return 1.
            else:
                return 0.

    def _compute_r_measure(self, answers, expected_answers):
        # Quite similar to recall.
        # If we have n expected answers, check how many of them are in the n first results of the query
        correct_answers_found = set(expected_answers).intersection(answers[0:len(expected_answers)])
        # Handle case where there is no expected answer : answer = [] => recall = 1, otherwise 0
        if len(expected_answers) != 0:
            return len(correct_answers_found) / float(len(expected_answers))
        else:
            return 1 if len(answers) == 0 else 0

    def _compute_f_measure(self, precision, recall):
        # precision and recall are already float, but better safe than sorry
        # When no answer is expected but we delivered at least one, then precision = recall = 0
        if precision == 0 and recall == 0:
            return 0
        else:
            return (1 + self.beta ** 2) * precision * recall / float(self.beta ** 2 * precision + recall)

    def _parse_queries_answers(self, queries_filename, answers_filename):
        queries = self.parse_queries(queries_filename)
        answers = self.parse_answers(answers_filename)

        query_answer = {}
        for query_id in queries:
            query_answer[queries[query_id]] = answers[query_id]

        return query_answer

    def parse_queries(self, queries_filename):
        with open(queries_filename, 'r') as f:
            self.lines = f.readlines()

        queries = {}
        current_line_number = 0
        while current_line_number < len(self.lines) - 1:
            current_line = self.lines[current_line_number]
            if current_line[:2] == '.I':
                query_id = int(current_line[3:5])
                current_line_number += 2
                end_line = self._find_line_query(current_line_number)
                # end_line contains the line where the .N block begins, so the query ends at the line before.
                queries[query_id] = ' '.join(self.lines[current_line_number:end_line]).replace('\n', ' ').replace('\t', ' ')

            current_line_number += 1

        return queries

    def parse_answers(self, answers_filename):
        with open(answers_filename, 'r') as f:
            self.lines = f.readlines()

        answers = defaultdict(list)

        for i in xrange(len(self.lines) - 1):
            query_id = int(self.lines[i][:2])
            document_id = int(self.lines[i][3:7])
            answers[query_id].append(document_id)

        return answers

    def _find_line_query(self, current_line_number):
        while self.lines[current_line_number][:2] != '.N':
            current_line_number += 1

        return current_line_number

a = Measures('sources/query.text', 'sources/qrels.text')
a.run_testing()
