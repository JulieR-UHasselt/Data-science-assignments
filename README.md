This folder is used for the project of the course 'Concepts of Data Science DL'.
This project is done by Julie Robbrecht and Shadi Hamdan.
The purpose of the project is to implement a bloom filter.

# Bloom Filter Performance Testing

## Overview

The purpose of this project is to implement a Bloom filter. The development of the Bloom filter is managed using version control hosted on [GitHub](https://github.com/JulieR-UHasselt/Data-science-assignments). The Bloom filter is implemented using an object-oriented approach. The performance testing suite measures the Bloom Filter's performance in terms of creation time, insertion time, search time, memory usage, and false positive rate using different dataset sizes. The results are visualized in a series of plots.

## Code Structure

### BloomFilter Class

The `BloomFilter` class implements a Bloom Filter to check if an item might be in a set. It includes the following methods:

- `__init__(self, dataset, P=0.01)`: Initializes the Bloom Filter with items from the dataset and a specified false positive rate.
- `_calculate_parameters(self)`: Calculates the size of the bit array and the number of hash functions based on the expected number of elements and the desired false positive rate.
- `insert_into_bit_array(self, element)`: Adds an item to the Bloom Filter.
- `search_bit_array(self, element)`: Checks if an item might be in the Bloom Filter.

### BloomFilterPerformanceTest Class

The `BloomFilterPerformanceTest` class tests the performance of the Bloom Filter. It includes the following methods:

- `__init__(self, dataset, dataset_sizes, num_runs=10, num_queries=1000)`: Sets up the performance test with the dataset, sizes to test, number of runs, and number of queries.
- `create_bf_from_dataset(self, dataset, P=0.01)`: Creates a Bloom Filter from the dataset.
- `search_bf(self, bf, dataset)`: Checks all items in the dataset against the Bloom Filter.
- `generate_random_words_not_in_dataset(self, dataset, num_words, length=10)`: Generates random words not in the dataset.
- `run_tests(self)`: Runs the performance tests on the Bloom Filter.
- `print_results(self)`: Prints the test results.
- `plot_results(self)`: Plots the test results.


## Performance Test Output

The performance tests generate plots for creation time, insertion time, memory usage, average search time, and false positive rate. The output is saved as an image with the name format `Pythonfilename_datasetname.png`.

## Results and Conclusion

Based on the performance test output provided in the image:

1. **Creation Time**: The creation time of the Bloom Filter increases linearly with the size of the dataset. This is expected as the Bloom Filter needs to initialize a bit array and hash functions for each element in the dataset.

2. **Insertion Time**: The insertion time also increases linearly with the dataset size. Each insertion involves multiple hash computations and bit manipulations, which scales with the number of elements.

3. **Memory Usage**: The memory usage increases linearly with the dataset size. This is because the size of the bit array is proportional to the number of elements in the dataset.

4. **Average Search Time**: The average search time remains relatively constant with slight variations. This indicates that the search operation in a Bloom Filter is efficient and does not depend heavily on the dataset size.

5. **False Positive Rate**: The false positive rate fluctuates slightly but remains close to the expected rate of around 1%. This demonstrates the effectiveness of the Bloom Filter in maintaining a low false positive rate while being space-efficient.

Overall, the performance tests show that the Bloom Filter scales well with increasing dataset sizes, providing efficient insertion and search operations while maintaining reasonable memory usage and false positive rates.

## Datasets Reference
### Words Data Source

The english words dataset `English_words.txt` contains over 479,000 English words and is sourced from the "dwyl/english-words" repository on GitHub.

- ["English Words Dataset."](https://github.com/dwyl/english-words/blob/master/words.txt) GitHub, dwyl. Accessed June 21, 2024.

### Genome Sequences Data Source

The genome sequences dataset `DNA_sequences.txt` includes 2000 records and can be found in the "genome" repository by MuhammadShan7 on GitHub.

- ["Genome Sequences Dataset."](https://github.com/MuhammadShan7/genome/blob/main/sequences.txt) GitHub, MuhammadShan7. Accessed June 21, 2024.


## Dataset File Formatting Guidelines

The dataset files to run with this code should follow:

### General Guidelines:

- Each line should contain a single string of words or DNA sequences.
- Ensure there are no additional columns, white spaces, or special characters in the file.

## Usage

To run the performance test, use the following command:
1. **Navigate to the Correct Directory**
   - In your terminal, use the `cd` command to navigate to the directory containing your `Bloomfilter_performance.py` script.

        ```bash
        cd /path/to/your/project/directory
        ```


2. **Run the Performance Test**

        ```bash
        python3 <Python_file> <datafile_path>
        ```


3. **Example:**

        ```bash
        python3 <Python_file> <datafile_path>
        ```


## Course Information

This project is a part of the course "Concept of Data Science - Distance learning" and demonstrates the practical application of data structures in implementation of the bloom filter.
