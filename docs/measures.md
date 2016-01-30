Measures
========


This is the results of the MAP value, as given by the script `measures.py` with all different parameters.

Note that boolean research has not been taken into account since the queries are not under FNC.  
Note also that, given that the proportional research does not rely on the ponderation of the reverse index, we don't need to do multiple tests for different ponderations for the reverse index.

Probabilistic research
----------------------

The only parameter was the method used for treating the probability that the document is relevant. It has three values, `constant`, `proportional`, and `log_proportional`.

| param value | MAP value |
|-------------|-----------|
|constant     | 0.1486    | 
|proportional | 0.1795    |
|log_proportional | 0.1778|

Average research time: 34 ms.


Vectorial Research
------------------

The only parameter was the similarity method. It could be one of `cosine`, `dice`, `jaccard`, `overlap`.
We also have to take into account the ponderation of the reverse index, which could be either of `tf_idf`, `normal_tf_idf`, `normal_frequency`.
We just show here the MAP value.


|     .     | tf_idf   | normal_tf_idf | normal_frequency |
|-----------|----------|---------------|------------------|
| cosine    | 0.1887   | 0.1106        | 0.0511           |
| dice      | 0.1656   | 0.0995        | 0.0554           |
| jaccard   | 0.1656   | 0.0995        | 0.0554           |
| overlap   | 0.1966   | 0.1443        | 0.0667           |

Average research time: 49 ms.

As expected, dice and jaccard methods are really similar. Moreover, the normal frequency ponderation seems highly unefficient, whereas the overlap similarity method looks promising. 


Boolean research
----------------

Average research time on queries with 5 OR terms and 2 AND terms each: 2 ms.
The boolean query is much faster for several reasons. First, there are fewer words to stem, which is one of the slowest operations. Second, it is optimized when sets of results are small, which is not the case for other research methods.
