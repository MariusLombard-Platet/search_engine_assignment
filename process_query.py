from stemming import PorterStemmer
import re


class Process_query:

    def __init__(self, stop_list_filename, format_type='vectorial'):
        self.stop_list = map(str.rstrip, open(stop_list_filename, 'r').readlines())
        self.stemmer = PorterStemmer()
        self.format_type = format_type

    def format_query(self, query):
        if self.format_type == 'vectorial' or self.format_type == 'probabilistic':
            return self._create_vectorial_query_from_string(query)
        elif self.format_type == 'boolean':
            return self._create_boolean_query_from_json(query)
        else:
            raise ValueError('Unsupported query type!')

    def _create_vectorial_query_from_string(self, query_string):
        return self._vectorial_stem_elements_from_list(
                self._remove_common_words_from_list(
                    re.findall('\w+', query_string.lower())
                )
            )

    def _create_boolean_query_from_json(self, query_string):
        """
        We only accept NDF queries, ie, a disjunction of conjunctions of terms (possibly negated with NOT).
        The valid accepted format is a string of NDF form.
        Examples:
            'computer AND series OR NOT conclusion AND testing'
            'study OR preprocessing'
            'IBM AND simulation'

        Query will be processed by a stemmer and common words will be removed, so there is no need to put them into the query.
        Empty list queries or clauses will return nothing.
        For instance, [[], ['another', 'nonrational', 'model']] is equivalent to [['another', 'nonrational', 'model']],
        which, after stemming + common-words removal, will give [['nonrat', 'model']]
        """
        query_list = self._byteify(map(lambda x: x.split(' and '), query_string.split(' or ')))

        if not self._check_valid_query(query_list):
            raise ValueError('The query does not have a valid format')

        return self._sanitize_boolean_query(query_list)

    def _byteify(self, input):
        """
        Transforms unicode objects from JSON decode to UTF-8 ones.
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

    def _check_valid_query(self, query_list):
        if type(query_list) is not list:
            return False

        for element in query_list:
            if type(element) is not list or not self._check_only_strings_in_list(element):
                return False

        return True

    def _check_only_strings_in_list(self, element_list):
        for element in element_list:
            if type(element) is not str:
                return False

        return True

    def _sanitize_boolean_query(self, query_list):
        # Stem the elements, remove the common ones
        # For speed reasons, first remove common words, then stem and remove common words
        return map(lambda element:
                   self._boolean_stem_elements_from_list(
                       self._boolean_remove_common_words_from_list(
                           element
                       )
                   ), query_list)

    def _boolean_remove_common_words_from_list(self, word_list):
        # print '_boolean_remove_common_words_from_list', word_list
        return [element for element in word_list if not self._boolean_should_delete(element)]

    def _vectorial_stem_elements_from_list(self, word_list):
        return map(lambda x: self.stemmer.stem(x, 0, len(x) - 1), word_list)

    def _boolean_stem_elements_from_list(self, word_list):
        # print '_boolean_stem_elements_from_list', word_list
        for i in xrange(len(word_list)):
            if self._is_real_word(word_list[i]):
                word_list[i] = self.stemmer.stem(word_list[i], 0, len(word_list[i]) - 1)
            else:
                word_list[i] = 'not ' + self.stemmer.stem(word_list[i][4:], 0, len(word_list[:4]) - 1)

        return word_list

    def _stem_elements_from_list(self, query_words):
        return map(lambda x: self.stemmer.stem(x, 0, len(x) - 1), query_words)

    def _remove_common_words_from_list(self, query_words):
        return [word for word in query_words if word not in self.stop_list]

    def _boolean_should_delete(self, element):
        if self._is_real_word(element):
            real_element = element
        else:
            real_element = element[4:]

        return real_element in self.stop_list

    def _is_real_word(self, element):
        return element[:4] != 'not '
