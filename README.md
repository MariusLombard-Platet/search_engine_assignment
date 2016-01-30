Final Project
=============


The source code is written in Python 2.

The code is self-documented, but you will find useful info in the [docs/](docs/) folder.

To launch the program : simply launch main.py, after having installed the dependecies (see below). You can change the config parameters in the config.ini file.

Dependencies
------------

For this program to run, you will need to install several libraries.

Run `pip install BTree configparser dill` from command line (you need to install pip first)

You will also need to unzip the [CACM collection](http://ir.dcs.gla.ac.uk/resources/test_collections/cacm/cacm.tar.gz), in `sources` folder. Your folder must look like:
```
├── search-engine-assignment
└── sources
    ├── README
    ├── cacm.all
    ├── cite.info
    ├── common_words
    ├── qrels.text
    └── query.text
```

Parameters
----------

All parameters are written in the `config.ini` file. You may change them to your needs. If a parameter is not valid, it is silently defaulted
(default is vectorial search on normal tf-idf with cosine similarity). After changing the parameters, you need to quit the program if you were running it. Both `main.py` and `mesures.py` rely on this config file.

Measures
--------

Just run `measures.py` to get a whole set of measures for your current config. Warning : this will give strange results for boolean search, since the queries are not in NDF. See [docs/measures.md](measures.md) for more details.

Reverse index
-------------

The reverse index has been implemented on CACM database only. It can support various types of ponderation, and is saved in the data/ folder for future uses. See [docs/reverse_index_construction.md](docs/reverse_index_construction.md) for more details.

Boolean Search
--------------

Boolean search **must** be typed as NDF, WITHOUT parenthesis, such as : "term1 AND term2 AND NOT term3 OR term1 AND term4". AND/OR/NOT can be lowercase. You cannot search for term AND/OR/NOT, as they are key values. They are nonrelevant anyway and automatically removed from both query and documents.

Results are ranked according to the Extended Boolean Search ranking (see [docs/search.md](docs/search.md) for more infos).


Vectorial Search
----------------

A vectorial search can be virtually anything. Results are ranked by their similarity. See [docs/search.md](docs/search.md) for more details.


Probabilistic search
--------------------

In the same way, a probabilistic query can be anything. Results are ranked by their RSV. See [docs/search.md](docs/search.md) for more details.
