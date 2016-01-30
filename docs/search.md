Here, you will find more infos about how research is done, for every different type of seach.

Generalities about search and queries
-------------------------------------

Common words (such as described in the file `common_words`) are automatically removed. Plus, every term is stemmed.


Boolean Search
--------------

Boolean search **must** be typed as NDF, WITHOUT parenthesis, such as : "term1 AND term2 AND NOT term3 OR term1 AND term4". AND/OR/NOT can be lowercase. You cannot search for term AND/OR/NOT, as they are key values. They are nonrelevant anyway and automatically removed from both query and documents.

Results that match the boolean query are then ordered with [Extended Boolean Search](http://www.wikiwand.com/en/Extended_Boolean_model) ranking (even if the search in itself is pure boolean).  
Custom ponderation has been made for terms with keyword NOT (since EBS do not take them in account), which you can change in the config.

Warning : given that we use EBS ranking, the reverse index must be normalized. As a consequence, you cannot use boolean search with a non-normalized reverse index (ie, tf_idf. Use normal tf_idf or normal_frequency instead).


Vectorial search
----------------

There are several available similarities : cosine, dice, jaccard, overlap. Overlap gives slightly better results.


Probabilistic search
--------------------

There are several estimations of the probability that the document is relevant for a given term. They are listed, in `config.ini`, by `constant`, `proportional`, and `log_propotional`.

* `constant` means that the document has 50% chances of being relevant
* `proportional` means that the probability for the document to be relevant is proportional the the probability of the term in the corpus (occurences of term / sum of all terms occurences)
* `log_propotional` is the same, but with logs (log10(occurences of term) / log10(sum of all occurences))
