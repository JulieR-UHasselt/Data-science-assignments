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
- `search_bf(self, bf, dataset)`: Checks all items in the dataset against the Bloom Filter.
- `search_bit_array(self, element)`: Checks if an item might be in the Bloom Filter.

### BloomFilterPerformanceTest Class

The `BloomFilterPerformanceTest` class tests the performance of the Bloom Filter. It includes the following methods:

- `__init__(self, dataset, dataset_sizes, num_runs=10, num_queries=1000)`: Sets up the performance test with the dataset, sizes to test, number of runs, and number of queries.
- `create_bf_from_dataset(self, dataset, P=0.01)`: Creates a Bloom Filter from the dataset.
- `generate_random_words_not_in_dataset(self, dataset, num_words, length=10)`: Generates random words not present in the dataset.

## Performance Testing

The performance testing suite evaluates the effectiveness of the Bloom Filter in maintaining a low false positive rate while being space-efficient.

Overall, the performance tests show that the Bloom Filter scales well with increasing dataset sizes, providing efficient insertion and search operations while maintaining reasonable memory usage and false positive rates.

## Datasets Reference

### Words Data Source

The English words dataset `English_words.txt` contains over 479,000 English words and is sourced from the "dwyl/english-words" repository on GitHub.

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

This project is a part of the course "Concept of Data Science - Distance learning" and demonstrates the practical application of data structures in the implementation of the bloom filter.
