# Qdrant for embeddings search
This code allow us to generate a little example of how a Qdrant database should behaving in a real environment. To achieve this goal, we use a pre-trained model of Wikipedia, provided by OpenAI, with around 26.000 articles. 

## Who it works
The whole code is divided in key modules.

### Read data function
[Read data](./project/utils/read_data.py) function reads the information storage in a csv file and convert it into a Panda array.

> This process is CPU intensive because it needs to works with a lot of vectors. In this example, you can work with the full collection (26000 articles) or with the test collection (2000 articles).

### Create collection
The way of how Qdrant storages information is with collection, similar to the concept of tables is relational databases. In this scenario it is necesarry to create our collection using the module [create collection](./project/utils/create_collection.py)

### Load data function
[Load data](./project/utils/load_data.py) has the work of push the information into the data.

## How to execute
To execute this example you just need to run the run script

```ssh
$ bash run.bash
```

This script is going to install all the system requirements and Python libraries, creation of a virtual environment and execution of the database.