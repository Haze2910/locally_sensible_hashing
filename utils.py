import numpy as np
import pandas as pd
import time
from hashlib import sha1


# Define hash family parameterized by an index
def hash_fn(x, i):
    output_size = 8
    max_length = 20
    salt = str(i).zfill(max_length)[-max_length:]
    return sha1((x + salt).encode('utf-8')).digest()[-output_size:]

# Define the Jaccard similarity between two sets:
def jaccard_similarity(sig1, sig2):
    num_union = len(set(sig1).union(sig2))
    num_intersection = len(set(sig1).intersection(sig2))
    return num_intersection / num_union

# Define the nearest neighbors algorithm
def nearest_neighbors(shingles_list, threshold):
    similar_pairs = []
    for i in range (len(shingles_list)):
        for j in range (i + 1, len(shingles_list)):
            if jaccard_similarity(shingles_list[i], shingles_list[j]) >= threshold:
                similar_pairs.append((i, j))
    return similar_pairs
