Reverse index structure
=======================

The reverse_index is actually a class, which contains the reverse index.

Its structure is (evry item of this list is an attribute of the class):

* reverse_index: either `defaultdict(dict)` or `OOBTree`, depending on the conf.
    ```
    {
        term1: {
            document_id1: ponderation,
            document_id2: ponderation,
            ...
        },

        term2: {
            document_id4: ponderation,
            document_id5: ponderation,
            ...
        },

        ...
    }
    ```

* id_set: `set(doc_id1, doc_id2, ..., doc_idN)`: set of all documents id.

* idf: ```defaultdict(int)
    {
        term1: number of occurences of term1 in all documents,  
        term2: number of occurences of term2 in all documents,  
        ...
    }```

* other_infos: 
```
    {
        'ponderation_method': the method used for ponderation in reverse index (tf_idf, normal_tf_idf, normal_frequency),
        'number_of_documents': number of documents in the base (int),
        'norms': defaultdict(lambda: defaultdict(foat))
            {
                document_id1: {
                    'linear' : linear norm of document,
                    'quadratic': quadratic norm of document,
                },
                ...
            },
        'max_unnormalized_ponderation': {
            document_id1: max_ponderation1,
            ...
        } # Used for vectorial search with normal_tf_idf
    }
```
