Final Project
=============


The source code is written in Python 2.

To launch the program : simply launch main.py, after having installed the dependecies (see below)

Dependencies
------------

For this program to run, you will need :

* BTrees (`pip install btrees` on Unix/Mac, and Windows with a decent python machine (e.g. Anaconda). Otherwise : https://pypi.python.org/pypi/BTrees/)


Boolean Search
--------------

Boolean search **must** be typed as NCF, without parenthesis, such as : "term1 AND term2 AND NOT term3 OR term1 AND term4". AND/OR/NOT can be lowercase.
Results are ordered with Extended Boolean Search ranking (even if the search in itself is boolean).
Custom ranking has been made for terms with keyword NOT.