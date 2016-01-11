from parse_docs import Parse_cacm
from reverse_index_builder import Reverse_index_builder
from boolean_search import Boolean_search

Parser = Parse_cacm('sources/cacm.all', 'sources/common_words')
index = Parser.parse_file()
# print index

Reverse_index_builder = Reverse_index_builder(Reverse_index_builder.PONDERATION_TF_IDF)
reverse_index = Reverse_index_builder.create_reverse_index(index)


# print reverse_index.get_index()
print reverse_index.get('series')
# print reverse_index['recommendations']
# print reverse_index['preliminary']
# print reverse_index['series']


# boolean_search =  Boolean_search(reverse_index)
# print boolean_search.do_search('series')
