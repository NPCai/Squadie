# Squadie    [:headphones:](https://www.youtube.com/watch?v=yGl0rS-ZcV4)

A library for generating OpenIE tuples from QA pairs (e.g. the SQuAD dataset). It makes use of Spacy's dependency parser and many handcrafted algorithms to create 3-tuples (subject, relation, object tuples). Additional READMEs are in each subdirectory.

## Example Usage
From the /src directory:
```python
import vis
import spacy

nlp = spacy.load('en')
doc = nlp(n'What are two complexity classes between L and P?')
ans = ['NL and NC']
sentences = list(doc)

for sentence, answer in zip(sentences, ans):
	print(sentence, answer)
	print(vis.parse(sentence, answer), "\n\n")
```
Output:
```
What are two complexity classes between L and P? NL and NC
<NL and NC,are two complexity classes between,L and P>
```

## Why?

Like in other areas of NLP, we expect neural networks to improve over state-of-the-art rule-based systems in OpenIE. However, neural open information extraction has been hampered by a lack of training data. 

[Cui et al. (2018)](https://arxiv.org/abs/1805.04270) offers one solution to this problem. They build training data by bootstrapping from a rule-based system, [OpenIE-4](https://github.com/allenai/openie-standalone). However, despite only keeping >90% confidence tuples from OpenIE-4, many of these tuples are malformed or incorrect. After experimenting with OpenIE-4, we noticed that reported confidence isn't a good measure of tuple quality. Clone our repositiory, [Legacy Open IE](https://github.com/NPCai/Legacy-Open-IE), to experiment with Stanford OpenIE and OpenIE-4. 

Large QA datasets are available and contain *almost* the right schema. An extensive ruleset (based on dependency parsing) can successfully convert QA pairs to OpenIE tuples. This is an easier problem then OpenIE itself because the answer is guarenteed to be one element in the tuple. The remaining problem is to (1) extract the other two elements, and (2) determine which is the subject/relation/object. 

## Examples

```
What are two complexity classes between L and P? NL and NC
<NL and NC,are two complexity classes between,L and P>

What is the prize offered for finding a solution to P=NP? $1,000,000
<$1,000,000,the prize offered for finding a solution to,P = NP>

In what year did Edmond's characterize a "good" algorithm?
<Edmond 's,characterize a " good " algorithm In what year,1965>

In the most basic sense what did a Turing machine emulate? a computer
<a Turing machine,In the most basic sense emulate,a computer>

In what country is Normandy located? France
<Normandy,In what country located,France>

When were the Normans in Normandy? 10th and 11th centuries
<the Normans,were in Normandy,10th and 11th centuries>

Who was the Norse leader? Rollo
<the Norse leader,was,Rollo>

Who was the duke in the battle of Hastings? William the Conqueror
<William the Conqueror,was the duke in the battle of,Hastings>

Who ruled the duchy of Normandy? Richard I
<Richard I,ruled the duchy of,Normandy>
```

The parse algorithms cannot handle every type of question. In most cases when this happens parse() will return None. However, in some cases, malformed tuples may be returned.


## Overview

The main library is in vis.py in src. This file contains the algorithms that takes a QA pair and creates a logical 3-tuple. The canvas.py provides a helpful illustration of a dependency tree. See the subdirectories for more READMEs.

## Dependencies 

* spacy
* unittest
