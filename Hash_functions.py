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

# Snippet 3: Function to Create Hash Functions


def create_hash_functions(k):
    """
    Create k hash functions each with random seeds.

    Parameters:
    k (int): Number of hash functions to create.

    Returns:
    tuple: List of hash functions and their corresponding seeds.
    """
    # Generate k random seeds
    random_seeds = []
    for i in range(k):
        random_seeds.append(random.randint(0, 1000000))
    # Create an empty list to store hash functions
    hash_functions = []

    # Define a function that creates a hash function using a seed
    def create_hash_function_with_seed(seed):

        def hash_fn(item):
            # Convert the item to a string and concatenate with the seed
            return hash(str(item) + str(seed))
        return hash_fn

    # Create k hash functions using the random seeds
    for seed in random_seeds:
        hash_function = create_hash_function_with_seed(seed)
        hash_functions.append(hash_function)

    return hash_functions, random_seeds
