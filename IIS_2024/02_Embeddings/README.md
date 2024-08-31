## Vector Similarity
The foundation for this measurement lies in the dot product. But the issue with the dot product, when used in isolation, is that it can take on any value and is therefore difficult to interpret in absolute terms.

Another solution is to use Cosine Similarity, a normalized form of the dot product.
### Cosine Similarity formula
```
$$
Sc (U, V) = cos(θ) = \frac{u \cdot v}{||u|| \cdot ||v||}
$$
```
### Cosine Interpretation
Cosine similarity disregards the magnitude of both vectors. forcing the calculation between -1 and 1.
- A value of 1 means the angle between the two vectors is 0 degrees. In other words, the two vectors are similar because they point in the exact same direction. 
- A value of 0 means the angle between the two vectors is 90 degrees. In this case, the vectors are orthogonal and unrelated to each other.
- A value of -1 means the angle between the two vectors is 180 degrees. This is an interesting case where the vectors are dissimilar because they point in opposite directions.

## Embeddings 
Embeddings are a way to represent data such as words, text, images and audios in a numerical format that computational algorithms can more easily process.
Embeddings are dense vectors that characterize meaningful information about the objects that they encode.

### Word Embeddings
A word embedding is a vector that captures the semantic meaning of word. Ideally, words that are semantically similar in natural language should have embeddings that are similar to each other in the encoded vector space.

Popular algorithms to generate word embeddings are Word2vec and GloVe.

### Text Embeddings 
Text embeddings encode information about sentences and documents, not just individual words, into vectors. This allows you to compare larger bodies of text to each other. Because they encode more information than a single word embedding, text embeddings are a more powerful representation of information.

The best text embedding models are built using transformers, which leverage a mechanism known as attention. To oversimplify things, the attention mechanism helps create context-specific word embeddings that fuse into text embeddings.

## Encode Objects in Embeddings
### Virtual Environment
It's recommendable generate a virtual environment to work with different libraries.

#### Installation
First, you need to install Venv.
```ssh
$ pip install virtualenv
```

It's possible that maybe you need another library.

```ssh
$ sudo apt install python3-venv
```

#### Initialization

```ssh
$ python3 -m venv env
```

#### Turn on/off
To turn on the virtual environment you need to execute the following command.
```ssh
$ source env/bin/activate
```

And to turn off the virtual environment it's necessary to run the following command.
```ssh
$ deactivate
```

### Install SpaCy
SpaCy library is a general-purpose NLP and popular Python library.

```ssh
$ python3 -m pip install spacy 
```

> The generation of the SpaCy wheel using pep 517 is very slow.

### Word embedding example
With the purpose of generate an example of word embedding, we need to download a model with embeddings. For this exercise, you can download two English models
- Medium model has 20,000 pre-trained word embeddings: 
    ```ssh
    $ python3 -m spacy download en_core_web_md
    ```
- Large model: has 514,000 embeddings. 
    ```ssh
    $ python3 -m spacy download en_core_web_lg
    ```

Now, you can find an example of how works with word embedding in the file ```./word_embeddings.py``` and a programmed Cosine Similarity Function in ```cosine_similarity.py``` .

### Text embedding example
The most efficient way to generate text embeddings is to use pre-trained models. The SentenceTransformers library in Python is one of the best tools for this. You can install sentence-transformers with the following command:

```ssh
$ python -m pip install sentence-transformers
```
> We are going to work with "all-MiniLM-L6-v2" model. This is one of the smallest pre-trained models available, but it’s a great one to start with.

An example of text embedding can be fount in ```./text_embedding.py```. This code also uses the Cosine Similarity Function located in ```cosine_similarity.py``` .