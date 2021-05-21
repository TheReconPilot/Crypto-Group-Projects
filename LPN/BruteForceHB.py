import numpy as np
from math import sqrt

from rich import print
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
import time

from HBProtocol import HBOracle, HammingWeight


def HypothesisTest(lpn, candidate_s):
    """Hypothesis Test for a candidate secret key

    Args:
        lpn (HBOracle): An HBOracle object representing the lock  
        candidate_s (np.array): Array containing the candidate secret

    Returns:
        bool: Result of whether the lpn passed the Hypothesis Test or not
    """
    dimension = lpn.dimension
    error_rate = lpn.error_rate

    # Estimate of samples needed for test
    m = int((4 * dimension) / ((0.5 - error_rate)**2))

    # Estimate of Hamming Weight threshold
    t = (m * error_rate) + sqrt(dimension * m)
    
    # Draw the sample
    A, b = lpn.sample(m)
    
    # If Hamming Weight is less than threshold, test is passed
    if HammingWeight(A @ candidate_s + b) <= t:
        return True
    else:
        return False

# Adapted from: https://stackoverflow.com/a/66398108
def generate_binary(n, bs=[], arr=[]):
    """Generate all possible binary secrets of length n

    Args:
        n (int): Length of secrets
        bs (list, optional): Placeholder. Defaults to [].
        arr (list, optional): Placeholder. Defaults to [].

    Returns:
        np.array: Array containing all possible binary secrets of length n
    """
    if len(bs) == n:
        arr.append(bs)
    else:
        generate_binary(n, bs + [0])
        generate_binary(n, bs + [1])
        
    return np.array(arr)      

# Brute Force attack on HB
def BruteForceHB(lpn):
    """Brute Force attack on HB Protocol

    Args:
        lpn (HBOracle): HBOracle object representing the lock

    Returns:
        np.array: Secret key which passes the Hypothesis Test
    """

    # Generate all candidates
    candidates = generate_binary(lpn.dimension)

    table = Table()
    table.add_column("Candidate Key", justify="center", style="turquoise2")
    table.add_column("Hypothesis Test Result", justify="center", style="orange_red1")

    with Live(table, refresh_per_second=4):
        # Loop through all candidates
        for candidate in candidates:
            
            # Test a candidate
            if HypothesisTest(lpn, candidate):
                table.add_row(f"[bold][cornflower_blue]{candidate}", "[sea_green2]:heavy_check_mark: Passed")
                return candidate

            table.add_row(f"{candidate}", "✗ Failed")
            time.sleep(0.2)
    
    print("Could not find.")
    return None

# Driver code to test
def main():
    p = 0.125
    dim = 5
    bfs = np.random.randint(0, 2, dim)
    bflpn = HBOracle(bfs, p)


    print(Panel(f"[yellow2]Brute Force on HB Protocol\n[cyan3]Error Rate = {p}\nKey Length = {dim}\nSecret Key = {bfs}", 
                title="[yellow]HB Protocol", expand=False))
    

    print(f"[light_steel_blue]Found key:     {BruteForceHB(bflpn)}")
    print(f"[light_steel_blue]Actual secret: {bflpn.secret}")

if __name__ == "__main__":
    main()