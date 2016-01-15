from parse_docs import Parse_cacm
from reverse_index_builder import Reverse_index_builder
from boolean_search import Boolean_search
from vectorial_search import Vectorial_search
import time

t0 = time.time()

Parser = Parse_cacm('sources/cacm.all', 'sources/common_words')

t1 = time.time()
print 'parse init : ', t1 - t0
index = Parser.parse_file()

t2 = time.time()
print 'parsing : ', t2 - t1
# print index

Reverse_index_builder = Reverse_index_builder()

reverse_index = Reverse_index_builder.create_reverse_index(index)

t4 = time.time()
print 'rev_index : ', t4 - t2
# print reverse_index.get_index()
# print reverse_index.get('series')
# print reverse_index['recommendations']
# print reverse_index['preliminary']
# print reverse_index['series']


# boolean_search = Boolean_search(reverse_index)
# # print 'results to query "multiplexor OR nonrational OR series AND NOT conclusion" : ',
# print boolean_search.do_search('series OR conclusion')
vectorial_search = Vectorial_search(reverse_index)

print vectorial_search.do_search('testing hypothesis for assignment on web search with vectorial model')
t6 = time.time()
print 'search : ', t6-t4

print 'total : ', t6 - t0
