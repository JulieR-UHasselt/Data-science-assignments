import math
import hashlib


class BloomFilter:

    def __init__(self, dataset, P=0.01):
        self.word_count = len(dataset) # Counter of words inserted
        self.dataset = dataset
        self.P = P
        self._calculate_parameters()
        self.bit_array = [0] * self.m  # Initialize the bit array with zeros
        for element in dataset:
            self.insert_into_bit_array(element)

    # Function to Calculate Optimal Parameters
    def _calculate_parameters(self):
        """
        Calculate the size of bit array (m) & number of hash functions (k)
        based on the excepted number of elements in the dataset (word_count)
        and the desired probability of false positives (P).

        Returns:
        tuple: Size of the bit array (m) and number of hash functions (k).

        Formulas:
        m = - (n * log(P)) / (log(2)^2)
        k = (m / n) * log(2)
        """
        m_float = - (self.word_count * math.log(self.P)) / (math.log(2) ** 2)
        k_float = (m_float / self.word_count) * math.log(2)

        # Convert m_float to an integer, rounding up if needed
        self.m = int(m_float) + 1 if m_float > int(m_float) else int(m_float)
        # Convert k_float to an integer, rounding up if needed
        self.k = int(k_float) + 1 if k_float > int(k_float) else int(k_float)
        return self.m, self.k
    
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
            digest = hashlib.sha1((str(element) +
                                   str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            self.bit_array[index] = 1
 
    # Function to Search Elements in the Bloom filter
    def search_bit_array(self, element):
        """
        Search an element in the bit array.

        Parameters:
        element: The element to check in the bit array (can be any type).
        bit_array: A list representing the bit array.
        """   
        for i in range(self.k):
            digest = hashlib.sha1((str(element) +
                                   str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            if self.bit_array[index] == 0:
                return False
        return True
    
    def __repr__(self):
        return f"Bloom_Filter(size={len(self.bit_array)}, P={self.P}, dataset_size={len(self.dataset)})"

    def __str__(self):
        return f"Bloom Filter with {self.word_count} items and false positive rate {self.P}"


def create_BF_from_dataset(dataset, P=0.01):
    return BloomFilter(dataset, P)
