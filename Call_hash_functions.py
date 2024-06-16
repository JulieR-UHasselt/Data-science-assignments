import Hash_functions
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Hash_function.py <datafile_path>")
        sys.exit(1)

    dataset_filename = sys.argv[1]
    P = 0.01

    dataset= []
    datafile = open(dataset_filename, 'r')
    for data_item in datafile.readlines():
        if data_item[-1] == "\n":
            


    Bloom_Filter.setup_counter(dataset)
    for element in dataset:
        Bloom_Filter.insert_into_bit_array(element)
        Bloom_Filter.search_bit_array(element)

    # Print the calculated values
    print(f"{dataset} Dataset: Number of elements(n)={Bloom_Filter.n}, Bit array size(m)={Bloom_Filter.m}, "
        f"Number of hash functions(k)={Bloom_Filter.k}, Desired false positive probability(P)={P}")