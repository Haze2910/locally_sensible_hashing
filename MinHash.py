import numpy as np
from utils import hash_fn

class MinHash:
    """
    Given a set of shingles representing a document, generate a minhash signature

    Args:
        iterations (int): length of the signature, i.e. number of repetitions of the hash function/ permutations
        use_permutation (bool): flag to decide to use an hash function or the permutations to generate the signature
    """
    def __init__(self, iterations, use_permutations=False):
        self.iterations = iterations
        self.use_permutations = use_permutations

    def generate_signature(self, shingles):
        """
        Args: 
            shingles (list): list of shingles representing a document
        
        Output:
            signature (list): signature of the document
        """
        hash_values = np.zeros((self.iterations, len(shingles)), dtype=np.uint64)
        np.random.seed(420)

        for i in range(self.iterations):
            if not self.use_permutations:
                hashed_shingles = [int.from_bytes(hash_fn(str(shingle), i), byteorder="big") for shingle in shingles]
            else:
                hashed_shingles = np.random.permutation(len(shingles))
            hash_values[i] = hashed_shingles
        
        signature = np.full(self.iterations, np.inf, dtype=np.uint64)

        for i in range(self.iterations):
            for shingle_idx, shingle in enumerate(shingles):
                if shingle:
                    signature[i] = min(signature[i], hash_values[i][shingle_idx])
        return signature
