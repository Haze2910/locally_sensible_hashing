from utils import hash_fn, jaccard_similarity

class LSH:
    """
    Initialize the LSH algorithm that divides shingles in bands and rows and 
    hashes the bands in bins which represents similarity between them
    """
    def __init__(self, n_bands, threshold):
        self.n_bands = n_bands
        self.threshold = threshold

    def get_similar(self, signatures):
        """
        Given a list of signatures, apply LSH and return similar items basing on Jaccard similarity over a threshold

        Args:
            signatures (list): list of signatures of a collection

        Output:
            similar_pairs (list): list of tuples of similar documents
        """

        # Check the signature length splits correctly into the number of bands
        assert len(signatures[0]) % self.n_bands == 0

        n_rows = int(len(signatures[0]) / self.n_bands)
        bands = []

        # Split the signature matrix into n_bands bands
        for i in range(self.n_bands):
            start_row = i * n_rows
            end_row = (i + 1) * n_rows
            bands.append([signature[start_row:end_row] for signature in signatures])

        # Initialize the candidate set
        candidate_pairs = set()

        # For each band, apply hash function and put the bands mapped to the same value in the same bin
        for band in bands:
            
            # Different bucket for each band so we don't hash columns with the same vector into different band in the same bucket
            bucket = {}

            for sign_idx, signature in enumerate(band):

                # Compute the hash for the band of the signature
                hashed_band = hash_fn(str(signature), 100)

                # Store the signature index in the bucket of the hash
                if hashed_band in bucket:
                    bucket[hashed_band].append(sign_idx)
                else:
                    bucket[hashed_band] = [sign_idx]

            # Now take each pair of bands collisions as candidates
            for bin in bucket.values():
                if len(bin) > 1:
                    for i in range(len(bin)):
                        for j in range(i + 1, len(bin)):
                            candidate_pairs.add((bin[i], bin[j]))

        # Finally return the candidate pairs that have Jaccard similarity > threshold as similar pairs
        similar_pairs = []
        for pair in candidate_pairs:
            if jaccard_similarity(signatures[pair[0]], signatures[pair[1]]) >= self.threshold:
                similar_pairs.append(pair)

        return similar_pairs
