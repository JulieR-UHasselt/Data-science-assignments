# Snippet 1: Importing Required Libraries
import math
import random

# Snippet 2: Function to Calculate Optimal Parameters

"""
    Calculate the size of the bit array (m) and the number of hash functions (k).

    Parameters:
    n (int): Number of elements in the dataset.
    P (float): Desired probability of false positives.

    Returns:
    tuple: Size of the bit array (m) and number of hash functions (k).

    Formulas:
    m = - (n * log(P)) / (log(2)^2)
    k = (m / n) * log(2)
    """


def calculate_parameters(n, P):

    m_float = - (n * math.log(P)) / (math.log(2) ** 2)  # Size of the bit array
    k_float = (m_float / n) * math.log(2)  # Number of hash functions

    # Convert m_float to an integer, rounding up if needed
    m = int(m_float) + 1 if m_float > int(m_float) else int(m_float)
    # Convert k_float to an integer, rounding up if needed
    k = int(k_float) + 1 if k_float > int(k_float) else int(k_float)
    return m, k
