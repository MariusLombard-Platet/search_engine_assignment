Final Project
=============


The source code is written in Python 2.

To launch the program : simply launch main.py, after having installed the dependecies (see below). You can change the config parameters in the config.ini file.

Dependencies
------------

For this program to run, you will need to install several libraries.

Run `pip install BTree configparser dill` from command line (you need to install pip first)

You will also need to unzip the [CACM collection](http://ir.dcs.gla.ac.uk/resources/test_collections/cacm/cacm.tar.gz), in `sources` folder. Your folder must look like:
```
├── search-engine-assignment
└── cacm
    ├── README
    ├── cacm.all
    ├── cite.info
    ├── common_words
    ├── qrels.text
    └── query.text

```


Measures
--------

Just run `measures.py` to get a whole set of measures for your current config. Warning : this will give strange results for boolean search, since the queries are not in NCF form.



Boolean Search
--------------

Boolean search **must** be typed as NCF, WITHOUT parenthesis, such as : "term1 AND term2 AND NOT term3 OR term1 AND term4". AND/OR/NOT can be lowercase. You cannot search for term AND/OR/NOT, as they are key values. They are nonrelevant anyway and automatically removed from both query and documents.

Results are ranked according to the Extended Boolean Search ranking (see docs/ for more infos).


Vectorial Search
----------------

A vectorial search can be virtually anything. Results are ranked by their similarity.  


Probabilistic search
--------------------

In the same way, a probabilistic query can be anything. Results are ranked by their RSV.
