# Squadie

A library for generating OpenIE tuples from QA pairs (e.g. the SQuAD dataset). It makes use of Python's Spacy library's dependency parser and many handcrafted algorithms to create 3-tuples (subject, relation, object tuples). 

### Why?

The problem of open information extraction has been hampered by lack of large datasets. Luckily, QA datasets are more developed and contain the content and *almost* the right schema.

### Overview

The main library is in vis.py in src. This file contains the algorithms that takes a QA pair and creates a logical 3-tuple. The canvas.py provides a helpful illustration of a dependency tree.

### Dependencies

The spaCy library is used for their pre-trained word vectors, deep learning integration, and most importantly the dependency parser. The neural aspect of this project was done using pytorch.
