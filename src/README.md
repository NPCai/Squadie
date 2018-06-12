### vis.py

Contains the library for parsing question/answer pairs. The most important function is parse(), which calls all the specialized parse methods in roughly a generic to specific order. 

### test.py

This file contains test cases for the library (and thus shows usage of its functions). Note that we haven't made explicist asserts (the fact that we're using unittest is just for structure). We found *assert* statements to be too binary, when in reality many tuples are possible. Maybe we need a BLEU-score based testing framework?

### canvas.py

Used to see dependency trees.

### main.py

Used to generate tuples from the SQuAD 2.0 dataset.
