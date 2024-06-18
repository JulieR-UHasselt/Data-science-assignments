import math
import hashlib
import sys


class Bloom_Filter:

    def __init__(self, dataset, P=0.01):
        self.word_count = len(dataset)
        self.P = P
        self._calculate_parameters()
        self.bit_array = [0] * self.m
        for element in dataset:
            self.insert_into_bit_array(element)

    def _calculate_parameters(self):
        m_float = - (self.word_count * math.log(self.P)) / (math.log(2) ** 2)
        k_float = (m_float / self.word_count) * math.log(2)
        self.m = math.ceil(m_float)
        self.k = math.ceil(k_float)

    def insert_into_bit_array(self, element):
        for i in range(self.k):
            digest = hashlib.sha1(
                (str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            self.bit_array[index] = 1

    def search_bit_array(self, element):
        for i in range(self.k):
            digest = hashlib.sha1(
                (str(element) + str(i)).encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.m
            if self.bit_array[index] == 0:
                return False
        return True


def create_BF_from_dataset(dataset, P=0.01):
    return Bloom_Filter(dataset, P)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Hash_function.py <datafile_path>")
        sys.exit(1)

    dataset_filename = sys.argv[1]
    P = 0.01

    dataset = []
    with open(dataset_filename, 'r') as datafile:
        dataset = [line.strip() for line in datafile]

    bloom_filter = Bloom_Filter(dataset, P)

    # Example usage of the Bloom Filter
    for element in dataset:
        result = bloom_filter.search_bit_array(element)
        print(f"Element {element} is in the Bloom Filter: {result}")

    print(f"{len(dataset)} elements inserted. Bit array size: {
        bloom_filter.m}, Hash functions: {bloom_filter.k}")
