Here, you will find more infos about how research is done, for every different type of seach.

Generalities about search and queries
-------------------------------------

Common words (such as described in the file `common_words`) are automatically removed. Plus, every term is stemmed.


Boolean Search
--------------

Results are ordered with Extended Boolean Search ranking (even if the search in itself is boolean).  
Custom ranking has been made for terms with keyword NOT, which you can change in the config.

Warning : given that we use EBS ranking, the reverse index must be normalized. As a consequence, you cannot use boolean search with a non-normalized reverse index (ie, tf_idf. Use normal tf_idf or normal_frequency instead).


Vectorial search
----------------

There are several available similarities : cosine, dice, jaccard, overlap. Overlap gives slightly better results.


Probabilistic search
--------------------
Todo : implement other ponderation methods for p_i.
