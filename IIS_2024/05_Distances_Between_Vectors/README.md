# How distances between vectors are calculated
## What is a vector?
[Vector Basics](../01_Vectors_Basics/README.md) TODO

## What is vector similarity search?
Similarity search or Approximate Nearest Neighbor (ANN) search is the method of searching in a rapid and accurate way similar vectors that are closest in terms of distance; in other words, search vectors who had similar information.

The data of the vectors are generate through an embedding model (from OpenAI, Cohere or HuggingFace, etc.) that converts the content into small word chunks (the vector embeddings). Each word chunk is assigned with a numerical value and this process is known as tokenization. 
> Note: the meaning of each value in the array, depends on what machine learning model we use to generate them.

## Techniques to calculate the distance between the vectors

### Dot product
The dot product, also called scalar product, is a measure of how closely two vectors align, in terms of the directions they point. The measure is a scalar number that can be used to compare the two vectors and to understand the impact of repositioning one or both of them

$$
a \cdot b \displaystyle\sum_{k=i}^n a_ib_i
$$

### Cosine distance
Cosine distance is a measure of similarity between two non-zero vectors that evaluates the cosine of the angle between them. It's not a 'distance' in the traditional sense, but rather a metric that determines how vectors are oriented relative to each other, regardless of their magnitude. Picture two arrows starting from the same point; the smaller the angle between them, the more similar they are in direction.

$$
cos(θ) = \frac{u \cdot v}{||u|| \cdot ||v||}
$$

### Euclidean distance
Euclidean distance, often known as the L2 norm, is the most direct way of measuring the distance between two points or vectors, resembling the way we usually think about distance in the physical world. In other words, is like measuring the straightest and shortest path between two points in an n-dimensional plane. Imagine drawing a straight line between two points on a map; the Euclidean distance is the length of this line.

$$ 
d(p,q) = \sqrt{\displaystyle\sum_{k=i}^n (q_i - p_i)^2}
$$

### Manhattan distance
Manhattan distance, also known as L1 distance or taxicab distance is a way of calculating the distance between two points or vectors by summing the absolute differences of their coordinates.

$$
d(x,y) = \displaystyle\sum_{k=i}^n |x_i - y_i|
$$

### Hamming distance


## Sources
- [Understanding + Calculating the Distance Between Vectors](https://www.singlestore.com/blog/distance-metrics-in-machine-learning-simplfied/#:~:text=There%20are%20different%20techniques%20to,in%20a%20multi%2Ddimensional%20space.)
- [https://weaviate.io/blog/distance-metrics-in-vector-searc]('https://weaviate.io/blog/distance-metrics-in-vector-search')
- [Euclidean Distance and Manhattan Distance](https://www.youtube.com/watch?v=p3HbBlcXDTE)