import math
import hashlib
import tracemalloc
import matplotlib.pyplot as plt
import random
import timeit
import sys
import logging
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BloomFilter:
    """A Bloom Filter to check if an item might be in a set."""

    def __init__(self, dataset, P=0.01):
        """
        Initialize the Bloom Filter with items.

        Parameters:
            dataset (list): Items to add to the Bloom Filter.
            P (float): Desired false positive rate, default is 0.01.
        """
        self.word_count = len(dataset)
        self.P = P
        self._calculate_parameters()
        self.bit_array = [0] * self.m

        # Use ThreadPoolExecutor to parallelize the insertion of elements into the Bloom Filter.
        # This can significantly speed up the initialization for large datasets by utilizing multiple CPU cores.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.insert_into_bit_array, dataset)

    def _calculate_parameters(self):
        """
        Calculate the size of bit array (m) & number of hash functions (k)
        based on the expected number of elements in the dataset (word_count) and
        the desired probability of false positives (P).
        """
        m_float = - (self.word_count * math.log(self.P)) / (math.log(2) ** 2)
        k_float = (m_float / self.word_count) * math.log(2)
        self.m = int(m_float) + 1 if m_float > int(m_float) else int(m_float)
        self.k = int(k_float) + 1 if k_float > int(k_float) else int(k_float)

    def insert_into_bit_array(self, element):
        """
        Add an item to the Bloom Filter by setting bits at k positions
        determined by hashing the item k times.

        Parameters:
            element (str): The item to add.
        """
        for i in range(self.k):
            digest = hashlib.sha1(
                (str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            self.bit_array[index] = 1

    def search_bit_array(self, element):
        """
        Check if an item might be in the Bloom Filter by verifying that
        all k bits corresponding to the k hashes of the item are set.

        Parameters:
            element (str): The item to check.

        Returns:
            bool: True if the item might be in the set, False if it is definitely not.
        """
        for i in range(self.k):
            digest = hashlib.sha1(
                (str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            if self.bit_array[index] == 0:
                return False
        return True


class BloomFilterPerformanceTest:
    """A class to test the performance of the Bloom Filter."""

    def __init__(self, dataset, num_runs=10, num_queries=1000):
        """
        Set up the performance test.

        Parameters:
            dataset (list): The list of items to test with.
            num_runs (int): How many times to run the test (default is 10).
            num_queries (int): How many queries to make for false positives (default is 1000).
        """
        self.dataset = dataset
        self.num_runs = num_runs
        self.num_queries = num_queries
        self.creation_times = []
        self.average_search_times = []
        self.memory_usages = []
        self.false_positive_rates = []

    def create_bf_from_dataset(self, dataset, P=0.01):
        """
        Create a Bloom Filter from the dataset.

        Parameters:
            dataset (list): The list of items to add to the Bloom Filter.
            P (float): Desired false positive rate, default is 0.01.

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
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(bf.search_bit_array, dataset)

    def generate_random_words_not_in_dataset(self, dataset, num_words, length=10):
        """
        Create a list of random words not in the dataset.

        Parameters:
            dataset (list): The original dataset to ensure new words are not in it.
            num_words (int): Number of random words to generate.
            length (int): Length of each random word, default is 10.

        Returns:
            list: A list of random words not in the dataset.
        """
        dataset_set = set(dataset)
        random_words = set()
        characters = 'abcdefghijklmnopqrstuvwxyz'

        while len(random_words) < num_words:
            word = ''.join(random.choices(characters, k=length))
            if word not in dataset_set:
                random_words.add(word)

        return list(random_words)

    def run_tests(self):
        """
        Run the performance tests on the Bloom Filter.
        Measure creation time, search time, memory usage, and false positive rate.
        """
        for _ in range(self.num_runs):
            try:
                tracemalloc.start()
                creation_time = timeit.timeit(
                    lambda: self.create_bf_from_dataset(self.dataset), number=1)
                bf = self.create_bf_from_dataset(self.dataset)
                current, peak = tracemalloc.get_traced_memory()
            finally:
                tracemalloc.stop()

            memory_usage = current / 1_000_000  # Convert bytes to MB
            self.creation_times.append(creation_time)
            self.memory_usages.append(memory_usage)

            search_time = timeit.timeit(
                lambda bf=bf: self.search_bf(bf, self.dataset), number=1)
            average_search_time = search_time / len(self.dataset)
            self.average_search_times.append(average_search_time)

            false_positives = 0
            random_words = self.generate_random_words_not_in_dataset(
                self.dataset, self.num_queries)
            for test_element in random_words:
                if bf.search_bit_array(test_element):
                    false_positives += 1

            false_positive_rate = false_positives / self.num_queries
            self.false_positive_rates.append(false_positive_rate)

            del bf  # Explicitly delete the Bloom Filter object to free up memory

    def print_results(self):
        """
        Print the test results.
        Show creation time, memory usage, average search time, and false positive rate.
        """
        logger.info("Bloom Filter Performance Test Results:")
        for i in range(self.num_runs):
            logger.info(f"Run {i + 1}:")
            logger.info(f"  Creation Time: {self.creation_times[i]:.6f} seconds")
            logger.info(f"  Memory Usage: {self.memory_usages[i]:.6f} MB")
            logger.info(
                f"  Average Search Time: {self.average_search_times[i]:.6f} seconds"
            )
            logger.info(
                f"  False Positive Rate: {self.false_positive_rates[i] * 100:.2f}%"
            )
            logger.info("")

    def plot_results(self):
        """
        Plot the test results.
        Create plots for creation time, memory usage, average search time, and false positive rate.
        """
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.plot(range(self.num_runs), self.creation_times,
                 marker='o', linestyle='-', color='b')
        plt.xlabel('Run')
        plt.ylabel('Seconds')
        plt.title('Bloom Filter Creation Time')
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(range(self.num_runs), self.memory_usages,
                 marker='o', linestyle='-', color='r')
        plt.xlabel('Run')
        plt.ylabel('MB')
        plt.title('Memory Usage')
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(range(self.num_runs), self.average_search_times,
                 marker='o', linestyle='-', color='g')
        plt.xlabel('Run')
        plt.ylabel('Seconds')
        plt.title('Average Search Time')
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(range(self.num_runs), self.false_positive_rates,
                 marker='o', linestyle='-', color='m')
        plt.xlabel('Run')
        plt.ylabel('Rate')
        plt.title('False Positive Rate')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('bloom_filter_performance.png')
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python bloomfilter_performance.py <datafile_path>")
        sys.exit(1)

    dataset_filename = sys.argv[1]

    dataset = []
    try:
        with open(dataset_filename, 'r', encoding='latin1') as datafile:
            dataset = [line.strip() for line in datafile.readlines()]
            if not dataset:
                raise ValueError("The dataset is empty.")
            logger.info(f'Successfully read {len(dataset)} lines from the file.')
    except FileNotFoundError:
        logger.error(f'Error: File not found: {dataset_filename}')
        sys.exit(1)
    except ValueError as e:
        logger.error(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        sys.exit(1)

    performance_test = BloomFilterPerformanceTest(dataset)
    performance_test.run_tests()
    performance_test.print_results()
    performance_test.plot_results()
