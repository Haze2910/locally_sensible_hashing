import pandas as pd
import time

from MinHash import *
from Shingler import *
from LSH import *
from utils import *

def main():
  # Retrieve items titles
    items_df = pd.read_csv("items.csv")
    docs = items_df["Title"].tolist()

    # Set shingle's dimension and generate them
    k = 10
    shingler = Shingler(k)
    shingles_list = [shingler.generate_shingle(doc) for doc in docs]

    # Generate MinHash signature for each doc
    iterations = 50
    
    minhasher = MinHash(iterations)
    signatures = [minhasher.generate_signature(shingles) for shingles in shingles_list]

    # Compute similar items using LSH
    n_bands = 10
    threshold = 0.8
    lsh = LSH(n_bands, threshold)

    start_time = time.time()
    LSH_similar = lsh.get_similar(signatures)
    end_time = time.time()
    print(f"\nLSH with {n_bands} bands: time elapsed computing similar items: {end_time - start_time:.2f}s")
    print(f"Similar items found {len(LSH_similar)}:\n{LSH_similar}")


    # Compute similar items using nearest neighbors
    start_time = time.time()
    NN_similar = nearest_neighbors(shingles_list, threshold)
    end_time = time.time()
    print(f"\nNN: time elapsed computing similar items: {end_time - start_time:.2f}s")
    print(f"Similar items found {len(NN_similar)}:\n{NN_similar}")

    # Print intersection size of the two methods results
    print(f"\nIntersection: {len(set(LSH_similar).intersection(NN_similar))}")

if __name__ == "__main__":
  main()
    
    
