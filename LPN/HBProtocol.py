import numpy as np

class HBOracle():
    def __init__(self, secret, error_rate):
        self.secret = secret
        self.dimension = len(secret)
        self.error_rate = error_rate

    def sample(self, n):
        # Generate an matrix with random binary values
        A = np.random.randint(0, 2, size = (n, self.dimension))

        # Add Bernoulli noise
        rng = np.random.default_rng()
        e = rng.binomial(1, self.error_rate, n)
        
        # Compute b
        b = np.mod(A @ self.secret + e, 2)
        
        return A, b

def HammingWeight(x):
    """Compute the Hamming Weight of x

    Args:
        x (np.array): Array containing binary numbers

    Returns:
        int: Hamming Weight of x, which is the sum of non-zero elements
    """
    return np.mod(x, 2).sum()
    