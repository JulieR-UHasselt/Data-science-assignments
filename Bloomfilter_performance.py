import tracemalloc
import matplotlib.pyplot as plt
import random
import timeit
import sys
import logging
from Bloomfilter import BloomFilter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        dataset_set = set(dataset)
        random_words = set()
        characters = 'abcdefghijklmnopqrstuvwxyz'

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

                bf = BloomFilter(sample_dataset)  # Create the Bloom Filter
                creation_time = timeit.timeit(lambda: BloomFilter(sample_dataset), number=1)  # Measure creation time

                current, peak = tracemalloc.get_traced_memory()  # Measure memory usage
                tracemalloc.stop()

                memory_usage = current / 1_000_000  # Convert memory usage to megabytes (MB)
                self.results[size]['creation_times'].append(creation_time)
                self.results[size]['memory_usages'].append(memory_usage)

                insertion_time = timeit.timeit(lambda: [bf.add(element) for element in sample_dataset], number=1)
                self.results[size]['insertion_times'].append(insertion_time)

                # measure search time
                search_time = timeit.timeit(lambda: self.search_bf(bf, sample_dataset), number=1)  # Measure search time
                average_search_time = search_time / len(sample_dataset)  # Calculate average search time per item
                self.results[size]['average_search_times'].append(average_search_time)

                # check for false positives
                false_positives = 0  # Check for false positives
                random_words = self.generate_random_words_not_in_dataset(sample_dataset, self.num_queries)
                for test_element in random_words:
                    if bf.search_bit_array(test_element):
                        false_positives += 1

                false_positive_rate = false_positives / self.num_queries  # Calculate false positive rate
                self.results[size]['false_positive_rates'].append(false_positive_rate)

                del bf  # Delete the Bloom Filter to free up memory

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

        avg_creation_times = [sum(self.results[size]['creation_times']) /
                              len(self.results[size]['creation_times']) for size in sizes]
        avg_insertion_times = [sum(self.results[size]['insertion_times']) /
                               len(self.results[size]['insertion_times']) for size in sizes]
        avg_memory_usages = [sum(self.results[size]['memory_usages']) /
                             len(self.results[size]['memory_usages']) for size in sizes]
        avg_search_times = [sum(self.results[size]['average_search_times']) /
                            len(self.results[size]['average_search_times']) for size in sizes]
        avg_false_positive_rates = [sum(self.results[size]['false_positive_rates']) /
                                    len(self.results[size]['false_positive_rates']) for size in sizes]

        plt.figure(figsize=(14, 10))

        plt.subplot(2, 3, 1)
        plt.plot(sizes, avg_creation_times, marker='o', linestyle='-', color='b')
        plt.xlabel('Dataset Size')
        plt.ylabel('Creation Time (s)')
        plt.title('Bloom Filter Creation Time')

        plt.subplot(2, 3, 2)
        plt.plot(sizes, avg_insertion_times, marker='o', linestyle='-', color='c')
        plt.xlabel('Dataset Size')
        plt.ylabel('Insertion Time (s)')
        plt.title('Bloom Filter Insertion Time')

        plt.subplot(2, 3, 3)
        plt.plot(sizes, avg_memory_usages, marker='o', linestyle='-', color='r')
        plt.xlabel('Dataset Size')
        plt.ylabel('Memory Usage (MB)')
        plt.title('Memory Usage')

        plt.subplot(2, 3, 4)
        plt.plot(sizes, avg_search_times, marker='o', linestyle='-', color='g')
        plt.xlabel('Dataset Size')
        plt.ylabel('Average Search Time (s)')
        plt.title('Average Search Time')

        plt.subplot(2, 3, 5)
        plt.plot(sizes, avg_false_positive_rates, marker='o', linestyle='-', color='m')
        plt.xlabel('Dataset Size')
        plt.ylabel('False Positive Rate')
        plt.title('False Positive Rate')

        plt.tight_layout()
        plt.show()


def load_dataset(file_path):
    """
    Load the dataset from the specified file.

    Parameters:
        file_path (str): The path to the dataset file.

    Returns:
        list: The dataset loaded from the file.
    """
    dataset = []
    try:
        # Read the dataset file
        with open(file_path, 'r', encoding='latin1') as datafile:
            dataset = [line.strip() for line in datafile.readlines() if line.strip()]  # Remove empty lines
            if not dataset:
                raise ValueError("The dataset is empty.")
            print(f'Successfully read {len(dataset)} lines from the file.')
    except FileNotFoundError:
        print(f'Error: File not found: {file_path}')
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)
    return dataset

if __name__ == "__main__":
    """
    Main function to run the Bloom Filter performance tests.
    """
    # Check for correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python Bloomfilter_performance.py <datafile_path>")
        sys.exit(1)

    # Get the dataset file path from command-line arguments
    dataset_filename = sys.argv[1]

    # Load the dataset from the specified file
    dataset = load_dataset(dataset_filename)

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
