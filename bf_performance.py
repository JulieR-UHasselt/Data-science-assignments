import math
import hashlib
import tracemalloc
import matplotlib.pyplot as plt
import random
import timeit
import sys
import os


class BloomFilter:
    """A Bloom Filter to check if an item might be in a set."""

    def __init__(self, dataset, P=0.01):
        """
        Initialize the Bloom Filter with items.

        Parameters:
            dataset (list): Items to add to the Bloom Filter.
            P (float, optional): Desired false positive rate. Default is 0.01.

        This method sets up the Bloom Filter with the provided list of items,
        calculates the necessary size of the bit array and the number of hash functions,
        and starts with an empty bit array to which each item from the dataset is added.
        """
        self.word_count = len(dataset)
        self.P = P
        self._calculate_parameters()
        self.bit_array = [0] * self.m  # Create an empty bit array
        for element in dataset:
            self.insert_into_bit_array(element)  # Add each item to the bit array

    def _calculate_parameters(self):
        """
        Calculate the size of bit array (m) and number of hash functions (k).

        This is based on the expected number of elements in the dataset (word_count) and
        the desired probability of false positives (P).
        """
        m_float = - (self.word_count * math.log(self.P)) / (math.log(2) ** 2)
        k_float = (m_float / self.word_count) * math.log(2)
        # Round up to ensure the bit array is large enough
        self.m = int(m_float) + 1 if m_float > int(m_float) else int(m_float)
        # Round up to ensure we have enough hash functions
        self.k = int(k_float) + 1 if k_float > int(k_float) else int(k_float)

    def insert_into_bit_array(self, element):
        """
        Add an item to the Bloom Filter by setting bits at k positions determined by hashing the item k times.

        Parameters:
            element (str): The item to add.
        """
        for i in range(self.k):
            # Create a unique hash for each combination of element and i
            digest = hashlib.sha1((str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m  # Convert hash to an index within the bit array
            self.bit_array[index] = 1  # Set the bit at the calculated index

    def search_bit_array(self, element):
        """
        Check if an item might be in the Bloom Filter by verifying that all k bits corresponding
        to the k hashes of the item are set.

        Parameters:
            element (str): The item to check.

        Returns:
            bool: True if the item might be in the set, False if it is definitely not.
        """
        for i in range(self.k):
            # Create a unique hash for each combination of element and i
            digest = hashlib.sha1((str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m  # Convert hash to an index within the bit array
            if not self.bit_array[index]:  # If any bit is not set, the element is definitely not in the set
                return False
        return True  # All bits are set, so the element might be in the set


class BloomFilterPerformanceTest:
    """A class to test the performance of the Bloom Filter."""

    def __init__(self, dataset, dataset_sizes, num_runs=10, num_queries=1000):
        """
        Set up the performance test.

        Parameters:
            dataset (list): The list of items to test with.
            dataset_sizes (list): List of sizes of datasets to test with.
            num_runs (int, optional): How many times to run the test for each size. Default is 10.
            num_queries (int, optional): How many queries to make for false positives. Default is 1000.

        This method initializes the performance test with the dataset and different sizes to test,
        sets up how many times to run each test and how many queries to use for checking false positives,
        and prepares a results dictionary to store test outcomes.
        """
        self.dataset = dataset
        self.dataset_sizes = dataset_sizes
        self.num_runs = num_runs
        self.num_queries = num_queries
        self.results = {size: {'creation_times': [], 'insertion_times': [], 'average_search_times': [],
                               'memory_usages': [], 'false_positive_rates': []} for size in dataset_sizes}

    def create_bf_from_dataset(self, dataset, P=0.01):
        """
        Create a Bloom Filter from the dataset.

        Parameters:
            dataset (list): The list of items to add to the Bloom Filter.
            P (float, optional): Desired false positive rate. Default is 0.01.

        Returns:
            BloomFilter: A Bloom Filter initialized with the dataset.
        """
        return BloomFilter(dataset, P)

    def search_bf(self, bf, dataset):
        """
        Check all items in the dataset against the Bloom Filter.

        Parameters:
            bf (BloomFilter): The Bloom Filter to search with.
            dataset (list): The list of items to check.
        """
        for element in dataset:
            bf.search_bit_array(element)  # Search each element in the Bloom Filter

    def generate_random_words_not_in_dataset(self, dataset, num_words, length=10):
        """
        Create a list of random words not in the dataset.

        Parameters:
            dataset (list): The original dataset to ensure new words are not in it.
            num_words (int): Number of random words to generate.
            length (int, optional): Length of each random word. Default is 10.

        Returns:
            list: A list of random words not in the dataset.

        This method generates random words not in the given dataset. It is useful for testing, especially for
        evaluating the Bloom Filter's false positive rate.
        """
        dataset_set = set(dataset)  # Convert the dataset to a set for faster lookups
        random_words = set()
        characters = 'abcdefghijklmnopqrstuvwxyz'  # Characters to use for generating random words

        while len(random_words) < num_words:
            word = ''.join(random.choices(characters, k=length))  # Generate a random word
            if word not in dataset_set:  # Ensure the word is not in the dataset
                random_words.add(word)

        return list(random_words)

    def run_tests(self):
        """
        Run the performance tests on the Bloom Filter.

        Measure creation time, insertion time, search time, memory usage, and false positive rate.
        """
        for size in self.dataset_sizes:
            sample_dataset = self.dataset[:size]  # Take a sample of the dataset of the given size
            for _ in range(self.num_runs):
                tracemalloc.start()  # Start measuring memory usage

                bf = self.create_bf_from_dataset(sample_dataset)  # Create the Bloom Filter
                creation_time = timeit.timeit(lambda: self.create_bf_from_dataset(
                    sample_dataset), number=1)  # Measure creation time

                current, peak = tracemalloc.get_traced_memory()  # Measure memory usage
                tracemalloc.stop()

                memory_usage = current / 1_000_000  # Convert memory usage to megabytes (MB)
                self.results[size]['creation_times'].append(creation_time)
                self.results[size]['memory_usages'].append(memory_usage)

                insertion_time = timeit.timeit(lambda: [bf.insert_into_bit_array(element)
                                                        for element in sample_dataset], number=1)
                self.results[size]['insertion_times'].append(insertion_time)

                search_time = timeit.timeit(lambda: self.search_bf(bf, sample_dataset),
                                            number=1)  # Measure search time
                average_search_time = search_time / len(sample_dataset)  # Calculate average search time per item
                self.results[size]['average_search_times'].append(average_search_time)

                false_positives = 0  # Check for false positives
                random_words = self.generate_random_words_not_in_dataset(sample_dataset, self.num_queries)
                for test_element in random_words:
                    if bf.search_bit_array(test_element):
                        false_positives += 1

                false_positive_rate = false_positives / self.num_queries  # Calculate false positive rate
                self.results[size]['false_positive_rates'].append(false_positive_rate)

                del bf  # Delete the Bloom Filter to free up memory

    def measure_creation_time_and_memory(self, sample_dataset):
        """
        Measure the creation time and memory usage of the Bloom Filter.

        Parameters:
            sample_dataset (list): The dataset to initialize the Bloom Filter with.

        Returns:
            tuple: Creation time, memory usage, and the created Bloom Filter.

        This method measures how long it takes to create the Bloom Filter and how much memory it uses.
        It uses tracemalloc to track memory usage and returns the creation time, memory usage, and the Bloom Filter itself.
        """
        try:
            tracemalloc.start()  # Start tracking memory usage
            bf = self.create_bf_from_dataset(sample_dataset)  # Create the Bloom Filter
            creation_time = timeit.timeit(lambda: self.create_bf_from_dataset(sample_dataset), number=1)
            current, peak = tracemalloc.get_traced_memory()  # Get the current memory usage
        finally:
            tracemalloc.stop()  # Stop tracking memory usage
        memory_usage = current / 1_000_000  # Convert bytes to MB
        return creation_time, memory_usage, bf  # Return the creation time, memory usage, and the Bloom Filter

    def measure_insertion_time(self, bf, sample_dataset):
        """
        Measure the insertion time for the dataset.

        Parameters:
            bf (BloomFilter): The Bloom Filter to insert into.
            sample_dataset (list): The dataset to insert.

        Returns:
            float: The insertion time.

        This method measures how long it takes to add all items from the dataset to the Bloom Filter.
        """
        return timeit.timeit(lambda: [bf.insert_into_bit_array(element) for element in sample_dataset], number=1)

    def measure_search_time(self, bf, sample_dataset):
        """
        Measure the search time for the dataset.

        Parameters:
            bf (BloomFilter): The Bloom Filter to search in.
            sample_dataset (list): The dataset to search.

        Returns:
            float: The average search time per element.

        This method measures how long it takes to search for each item in the dataset within the Bloom Filter.
        It returns the average search time per item.
        """
        search_time = timeit.timeit(lambda: self.search_bf(bf, sample_dataset), number=1)
        return search_time / len(sample_dataset)  # Calculate average search time per element

    def measure_false_positive_rate(self, bf, sample_dataset):
        """
        Measure the false positive rate for the Bloom Filter.

        Parameters:
            bf (BloomFilter): The Bloom Filter to test.
            sample_dataset (list): The dataset used to generate random words not in it.

        Returns:
            float: The false positive rate.

        This method measures how often the Bloom Filter incorrectly says a random word (not in the dataset) is present.
        It generates random words and checks them against the Bloom Filter, returning the rate of these false positives.
        """
        false_positives = 0
        random_words = self.generate_random_words_not_in_dataset(sample_dataset, self.num_queries)
        for test_element in random_words:
            if bf.search_bit_array(test_element):
                false_positives += 1
        return false_positives / self.num_queries  # Calculate and return the false positive rate

    def print_results(self):
        """
        Print the test results.

        Show creation time, insertion time, memory usage, average search time, and false positive rate.
        """
        for size in self.dataset_sizes:
            print(f"Results for dataset size {size}:")
            creation_time = sum(self.results[size]['creation_times']) / len(self.results[size]['creation_times'])
            insertion_time = sum(self.results[size]['insertion_times']) / len(self.results[size]['insertion_times'])
            memory_usage = sum(self.results[size]['memory_usages']) / len(self.results[size]['memory_usages'])
            average_search_time = sum(self.results[size]['average_search_times']) / \
                len(self.results[size]['average_search_times'])
            false_positive_rate = sum(self.results[size]['false_positive_rates']) / \
                len(self.results[size]['false_positive_rates'])
            print(f"  Average Creation Time: {creation_time:.6f} seconds")
            print(f"  Average Insertion Time: {insertion_time:.6f} seconds")
            print(f"  Average Memory Usage: {memory_usage:.6f} MB")
            print(f"  Average Search Time: {average_search_time:.6f} seconds")
            print(f"  False Positive Rate: {false_positive_rate * 100:.2f}%")
            print()

    def plot_results(self):
        """
        Plot the test results.

        Create plots for creation time, insertion time, memory usage, average search time, and false positive rate.
        """
        sizes = self.dataset_sizes  # Dataset sizes used for the tests

        # Calculate average creation times for each dataset size
        avg_creation_times = [sum(self.results[size]['creation_times']) /
                              len(self.results[size]['creation_times']) for size in sizes]

        # Calculate average insertion times for each dataset size
        avg_insertion_times = [sum(self.results[size]['insertion_times']) /
                               len(self.results[size]['insertion_times']) for size in sizes]

        # Calculate average memory usages for each dataset size
        avg_memory_usages = [sum(self.results[size]['memory_usages']) /
                             len(self.results[size]['memory_usages']) for size in sizes]

        # Calculate average search times for each dataset size
        avg_search_times = [sum(self.results[size]['average_search_times']) /
                            len(self.results[size]['average_search_times']) for size in sizes]

        # Calculate average false positive rates for each dataset size
        avg_false_positive_rates = [sum(self.results[size]['false_positive_rates']) /
                                    len(self.results[size]['false_positive_rates']) for size in sizes]

        # Create a figure with a specified size
        plt.figure(figsize=(14, 10))

        # Plot for creation time
        plt.subplot(2, 3, 1)
        plt.plot(sizes, avg_creation_times, marker='o', linestyle='-', color='b')
        plt.xlabel('Dataset Size')
        plt.ylabel('Creation Time (s)')
        plt.title('Bloom Filter Creation Time')

        # Plot for insertion time
        plt.subplot(2, 3, 2)
        plt.plot(sizes, avg_insertion_times, marker='o', linestyle='-', color='c')
        plt.xlabel('Dataset Size')
        plt.ylabel('Insertion Time (s)')
        plt.title('Bloom Filter Insertion Time')

        # Plot for memory usage
        plt.subplot(2, 3, 3)
        plt.plot(sizes, avg_memory_usages, marker='o', linestyle='-', color='r')
        plt.xlabel('Dataset Size')
        plt.ylabel('Memory Usage (MB)')
        plt.title('Memory Usage')

        # Plot for average search time
        plt.subplot(2, 3, 4)
        plt.plot(sizes, avg_search_times, marker='o', linestyle='-', color='g')
        plt.xlabel('Dataset Size')
        plt.ylabel('Average Search Time (s)')
        plt.title('Average Search Time')

        # Plot for false positive rate
        plt.subplot(2, 3, 5)
        plt.plot(sizes, avg_false_positive_rates, marker='o', linestyle='-', color='m')
        plt.xlabel('Dataset Size')
        plt.ylabel('False Positive Rate')
        plt.title('False Positive Rate')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Save the figure to a file with a name based on the Python script and dataset filename
        script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        dataset_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        plt.savefig(f'{script_name}_{dataset_name}.png')

        # Display the plots
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bloomfilter_performance.py <datafile_path>")
        sys.exit(1)

    dataset_filename = sys.argv[1]

    dataset = []
    try:
        # Read the dataset file
        with open(dataset_filename, 'r', encoding='latin1') as datafile:
            dataset = [line.strip() for line in datafile.readlines() if line.strip()]  # Remove empty lines
            if not dataset:
                raise ValueError("The dataset is empty.")
            print(f'Successfully read {len(dataset)} lines from the file.')
    except FileNotFoundError:
        print(f'Error: File not found: {dataset_filename}')
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)

    # Define dataset sizes as percentages of the actual dataset size, testing the Bloom Filter with increasing data size.
    actual_dataset_size = len(dataset)
    dataset_percentages = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0]
    dataset_sizes = [int(actual_dataset_size * percentage) for percentage in dataset_percentages]

    # Create a performance test instance
    performance_test = BloomFilterPerformanceTest(dataset, dataset_sizes)
    # Run the performance tests
    performance_test.run_tests()
    # Print the results
    performance_test.print_results()
    # Plot the results
    performance_test.plot_results()
