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
        """
        Create a hash function using the provided seed.

        Parameters:
        seed (int): The seed used to create the hash function.

        Returns:
        function: A hash function that hashes an item with the given seed.
        """
        def hash_fn(item):
            # Convert the item to a string and concatenate with the seed
            return hash(str(item) + str(seed))
        return hash_fn

    # Create k hash functions using the random seeds
    for seed in random_seeds:
        hash_function = create_hash_function_with_seed(seed)
        hash_functions.append(hash_function)

    return hash_functions, random_seeds

# Snippet 4: Function to Add Elements to the Bit Array and Track Collisions


def insert_into_bit_array(element, bit_array, hash_functions, collision_tracker):
    """
    Add an element to the bit array using the given hash functions.

    Parameters:
    element: The element to add to the bit array (can be any type).
    bit_array: A list representing the bit array.
    hash_functions: A list of hash functions.
    collision_tracker: A dictionary to track collisions.
    """
    # Loop through each hash function
    for hash_fn in hash_functions:
        # Get the hash value of the element using the hash function
        hash_value = hash_fn(element)

        # Calculate the index by taking the modulus of the hash value with the length of the bit array
        index = hash_value % len(bit_array)

        # Check if the bit at the calculated index is already set (1)
        if bit_array[index] == 1:
            # If it is already set, it means there is a collision, so we track it
            if index not in collision_tracker:
                # Initialize the list if not already present
                collision_tracker[index] = []
            collision_tracker[index].append(element)

        # Set the bit at the calculated index to 1
        bit_array[index] = 1

# Snippet 5: Function to Print the Bit Array Status / this is only for visualization (can be removed later)


def print_bit_array_status(bit_array, element, hash_functions, dataset_name):
    """
    Print the bit array and the indices set by the hash functions for a specific element.

    Parameters:
    bit_array (list): The bit array.
    element (str): Element that was added.
    hash_functions (list): List of hash functions.
    dataset_name (str): Name of the dataset.
    """
    # Step 1: Calculate the indices set by the hash functions
    indices = []
    for hash_fn in hash_functions:
        # Calculate the index for the current hash function
        index = hash_fn(element) % len(bit_array)
        # Add the index to the list of indices
        indices.append(index)

    # Step 2: Create a string representation of the bit array
    bit_array_str = ''
    for bit in bit_array:
        if bit == 1:
            bit_array_str += '1'
        else:
            bit_array_str += '0'

    # Step 3: Count the number of 1's in the bit array
    num_ones = 0
    for bit in bit_array:
        if bit == 1:
            num_ones += 1

    # Step 4: Print the status of the bit array
    print(f"\nBit Array for {dataset_name} after Adding '{element}':")
    print("-" * 60)
    print(bit_array_str)
    print("-" * 60)
    print("Indexes set by hash functions: " + ' '.join(str(i)
          for i in indices))
    print(f"Number of 1's in the bit array: {num_ones}")

# Snippet 6: Function to Print Collisions


def print_collisions(collision_tracker):
    """
    Print collisions detected in the bit array.

    Parameters:
    collision_tracker (dict): Dictionary to track collisions.
    """
    print("\nCollisions:")
    for index, elements in collision_tracker.items():
        if len(elements) > 1:
            print(f"Index {index} is set by multiple elements: {elements}")
