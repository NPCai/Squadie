### vis.py

Contains the library for parsing question/answer pairs. The most important function is parse(), which calls all the specialized parse methods in roughly a generic to specific order. 

### test.py

This file contains test cases for the library (and thus shows usage of its functions). Note that we haven't made explicist asserts (the fact that we're using unittest is just for structure). We found *assert* statements to be too binary, when in reality many tuples are possible. Maybe we need a BLEU-score based testing framework?

### canvas.py

Used to see dependency trees.

### main.py

Used to generate JSON file ../data/qaTuples.json from the SQuAD 2.0 dataset. This file has a similar structure to the SQuAD JSON and contains questions, tuples, and contexts (i.e. the whole paragraph). The data is not yet segmented into sentence-tuple pairs for supervised training data. We generate this intermediate file because one might have other uses for the data, e.g. OKR, paragraph-level IE, etc.

### gen_supervised.py

Takes the data in ../data/qaTuples.json and changes it into sentence-tuples pairs suitable for supervised learning.
