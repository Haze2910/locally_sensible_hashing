from utils import hash_fn

class Shingler:
    """
    Given a document return a set of shingles of size k as output

    Args:
        k (int): size of each shingle
        hash (bool): flag to apply an hash function parameterized by a seed to the shingles
        seed (int): seed for the hash function
    """
    def __init__(self, k, hash=True, seed=100):
        self.k = k
        self.hash = hash
        self.seed = seed

    def generate_shingle(self, doc):
        """
        Args:
            doc (str): document to generate shingles from

        Output:
            shingles (set): set of shingles without repetitions
        """
        shingles = set()
        for i in range(len(doc) - self.k + 1):
            shingle = doc[i:i + self.k]
            if hash:
                shingle = hash_fn(shingle, self.seed)
            shingles.add(shingle)

        return shingles
