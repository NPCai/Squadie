# Squadie

A library for generating OpenIE tuples from QA pairs (e.g. the SQuAD dataset). It makes use of Python's Spacy library's dependency parser and many handcrafted rules to create 3-tuples (subject, relation, object tuples). 

### Why?

The problem of open information extraction has been hampered by lack of large datasets. Luckily, there QA datasets are more developed and contain the content and *almost* the right schema.

### Overview

The main library in in vis.py in src.
