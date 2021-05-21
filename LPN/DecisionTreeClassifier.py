import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

import time

from HBProtocol import HBOracle, HammingWeight

from rich import print
from rich.panel import Panel
from rich.traceback import install
install()

def DTC(lpn, tries=5, samples=10000):
    """Train and run a Decision Tree Classifier on the data

    Args:
        lpn (HBOracle): HBOracle object
        tries (int, optional): Number of runs. Defaults to 5.
        samples (int, optional): Number of samples to draw. Defaults to 10000.

    Returns:
        np.array: Array containing predicted secret
    """
    dt = DecisionTreeClassifier()

    # Run the whole process multiple times in case a run fails
    for i in range(tries):
        # Get samples
        A, b = lpn.sample(samples)

        A_train, test_a, b_train, test_b = train_test_split(A, b, test_size = 0.20)

        # Fit the tree
        dt.fit(A_train, b_train)

        # Testing tree
        test_pred_decision_tree = dt.predict(test_a)
        
        # Get the confusion matrix
        confusion_matrix = metrics.confusion_matrix(test_b, test_pred_decision_tree)
        
        matrix_df = pd.DataFrame(confusion_matrix)
        
        # Plot the result
        ax = plt.axes()
        sns.set(font_scale=1.3)
        plt.figure(figsize=(10,7))
        sns.heatmap(matrix_df, annot=True, fmt="g", ax=ax, cmap="magma")
        
        ax.set_title('Confusion Matrix - Decision Tree')
        ax.set_xlabel("Predicted label", fontsize =15)
        ax.set_ylabel("True Label", fontsize=15)

        # Close the extra empty plot that opens up
        plt.close(2)

        plt.show()
        
        # Print Report
        print("\n[bold][indian_red1]Classification Report")
        print(f"[dark_olive_green2]{metrics.classification_report(test_b, test_pred_decision_tree)}")

        # Predict the canonical unit vectors
        # (1, 0, 0, ..., 0)
        # (0, 1, 0, ..., 0)
        # ...
        # (0, 0, 0, ..., 1)
        s_candidate = dt.predict(np.eye(lpn.dimension))

        # Define threshold with a 2% breathing room
        threshold = int(samples * (lpn.error_rate + 0.02))

        # Check if the candidate solution's Hamming Weight is below threshold
        if HammingWeight(A @ s_candidate + b) < threshold:
            return s_candidate
            break
    else:
        print("Could not find a suitable candidate. Try running again or increase samples.")
        return None

def main():
    p = 0.125
    dimension = 12
    s = np.random.randint(0, 2, dimension)

    lpn = HBOracle(s, p)
    
    print(Panel(f"[yellow2]Decision Tree Classifier\n[cyan3]Error Rate = {p}\nKey Length = {dimension}\nSecret Key = {s}", 
                title="[yellow]HB Protocol", expand=False))
    
    print("[spring_green1]Training a Decision Tree Classifier")
    print("[medium_turquoise]Showing the Confusion Matrix")

    time.sleep(1)

    sdtc = DTC(lpn, tries=1, samples=100000)
    if sdtc is not None:
        print(f"[bold][light_steel_blue1]Key as per DTC:    {sdtc}")
        print(f"[thistle3]Actual secret key: {lpn.secret}")

if __name__ == "__main__":
    main()