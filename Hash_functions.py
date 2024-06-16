import math
import random
import hashlib
import sys


class Bloom_filter:

    def __init__(self, string):
        self._string = string
        self.m = None  # Size of the bit array
        self.k = None  # Number of hash functions
        self.bit_array = [0] * self.m  # Initialize the bit array with all zeros


    # Function to Calculate Optimal Parameters
    def calculate_parameters(self, n, P):
        """
        Calculate the size of bit array (m) & number of hash functions (k).

        Parameters:
        n (int): Excepted number of elements in the dataset.
        P (float): Desired probability of false positives.

        Returns:
        tuple: Size of the bit array (m) and number of hash functions (k).

        Formulas:
        m = - (n * log(P)) / (log(2)^2)
        k = (m / n) * log(2)
        """
        m_float = - (n * math.log(P)) / (math.log(2) ** 2)
        k_float = (m_float / n) * math.log(2)

        # Convert m_float to an integer, rounding up if needed
        self.m = int(m_float) + 1 if m_float > int(m_float) else int(m_float)
        # Convert k_float to an integer, rounding up if needed
        self.k = int(k_float) + 1 if k_float > int(k_float) else int(k_float)
        return self.m, self.k
    

    # # Function to Create Hash Functions
    # def create_hash_functions(self, k):
    #     """
    #     Create k hash functions each with random seeds.

    #     Parameters:
    #     k (int): Number of hash functions to create.

    #     Returns:
    #     tuple: List of hash functions and their corresponding seeds.
    #     """
    #     # Generate k random seeds
    #     self.random_seeds = [random.randint(0, 1000000) for i in range(k)]

    #     # Define a function that creates a hash function using a seed
    #     def create_hash_function_with_seed(seed):
    #         """
    #         Create a hash function using the provided seed.

    #         Parameters:
    #         seed (int): The seed used to create the hash function.

    #         Returns:
    #         function: A hash function that hashes an item with the given seed.
    #         """
    #         def hash_fn(item):
    #             # Convert the item to a string and concatenate with the seed
    #             return hash(str(item) + str(seed))
    #         return hash_fn

    #     # Create k hash functions using the random seeds
    #     self.hash_function = [create_hash_function_with_seed(seed) for seed in self.random_seeds]

    #     return self.hash_functions, self.random_seeds
    

    # Function to Add Elements to the Bloom Filter
    def insert_into_bit_array(self, element):
        """
        Add an element to the bit array using the given number hash functions
        and the size of the array.

        Parameters:
        element: The element to add to the bit array (can be any type).
        bit_array: A list representing the bit array.
        """
        for i in range(self.k):
            digest = hashlib.sha1((str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            self.bit_array[index] = 1

    
    # Function to Search Elements in the Bloom filter
    def search_bit_array(self, element):
        for i in range(self.k):
            digest = hashlib.sha1((str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            if self.bit_array[index] == 0:
                return False
        return True
            
            
            
            
    # dataset, dataset_name, P=0.01):
    #     """
    #     Process a dataset with hashing and collision detection.

    #     Parameters:
    #     dataset: A list of elements in the dataset.
    #     dataset_name: The name of the dataset.
    #     P: The desired probability of false positives (default is 0.01).

    #     Returns:
    #     None
    #     """
    #     # 1: Calculate the number of elements in the dataset
    #     n = len(dataset)

    #     # 2: Calculate the size of the bit array (m) and the number of hash functions (k)
    #     m, k = calculate_parameters(n, P)

    #     # Print the calculated values
    #     print(f"{dataset_name} Dataset: Number of elements(n)={n}, Bit array size(m)={m}, "
    #         f"Number of hash functions(k)={k}, Desired false positive probability(P)={P}")

    #     # 3: Create hash functions for the dataset
    #     hash_functions, seeds = create_hash_functions(k)

    #     # 6: Process each item in the dataset
    #     for item in dataset:
    #         # Add the item to the bit array using the hash functions
    #         insert_into_bit_array(
    #             item, bit_array, hash_functions, collision_tracker)

    #         # Print the current status of the bit array
    #         print_bit_array_status(bit_array, item, hash_functions, dataset_name)

    #     # 7: Print the hash functions and their corresponding seeds (this can be removed too)

    #     # Print a header to indicate that we are showing the hash functions and their seeds
    #     print(f"\nHash functions for {dataset_name} with seeds:")

    #     # Loop through the range of the number of hash functions
    #     for index in range(len(hash_functions)):
    #         # Get the hash function and seed at the current index
    #         hash_fn = hash_functions[index]
    #         seed = seeds[index]

    #         # Print the hash function number and its seed
    #         print(f"Hash function {i}: Seed = {seed}")

    #         # Increment the counter
    #         i += 1




#TO DO
#Collision

            # Check if the bit at the calculated index is already set (1)
            if bit_array[index] == 1:
                # If it is already set, it means there is a collision, so we track it
                if index not in collision_tracker:
                    # Initialize the list if not already present
                    collision_tracker[index] = []
                collision_tracker[index].append(element)

# Snippet 6: Function to Print Collisions


def print_collisions(collision_tracker):
    """
    Print collisions detected in the bit array.

    Parameters:
    collision_tracker (dict): Dictionary to track collisions.
    """
    print("\nCollisions:")
    if not collision_tracker:
        print("None")
    else:
        for index, elements in collision_tracker.items():
            if len(elements) > 1:
                print(f"Index {index} is set by multiple elements: {elements}")

# 8: Print the collisions detected in the bit array
    print_collisions(collision_tracker)


#To remove
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
