import spacy
from cosine_similarity import compute_cosine_similarity

nlp = spacy.load("en_core_web_lg")

dog_embedding = nlp.vocab["dog"].vector
cat_embedding = nlp.vocab["cat"].vector
apple_embedding = nlp.vocab["apple"].vector
tasty_embedding = nlp.vocab["tasty"].vector
delicious_embedding = nlp.vocab["delicious"].vector
truck_embedding = nlp.vocab["truck"].vector


print(compute_cosine_similarity(dog_embedding, cat_embedding))

print(compute_cosine_similarity(delicious_embedding, tasty_embedding))

print(compute_cosine_similarity(apple_embedding, delicious_embedding))

print(compute_cosine_similarity(dog_embedding, apple_embedding))

print(compute_cosine_similarity(truck_embedding, delicious_embedding))