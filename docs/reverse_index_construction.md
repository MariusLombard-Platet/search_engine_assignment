Reverse index builder
=====================


Building the reverse index every time is really long, so we don't do it. Instead, every time we start the program, we check whether there exists a backup of a reverse index with exactly the same parameters, which are listed in [Reverse_index] part of the config.

(Actually, this is not quite true since I never fully tested the code with BTrees, because the index building is far too long. As a consequence, BTree might not totally work, and BTrees reverse index are saved at the exact same filename as dict reverse indexes of same config.)

If the reverse index exists, then it is loaded, which easily avoids a few seconds of latency at the beginning of the script.

I chose to use a dictionnary, because of its simplicity of use. Plus, a dictionnary is basically a hash table, so all access are quite fast.

Also, when a document is processed, the common words are removed, and all the remaining words are stemmed. This implies that all queries must follow the same treatment of stemmification + common word removal
