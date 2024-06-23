from Bloomfilter import BloomFilter


# 1. Importing datasets to create bloomfilters
## Importing different types of data

### 1. URLs
urls = [
    "http://example.com",
    "https://example.org",
    "http://test.com",
    "https://mywebsite.net",
    "http://anotherexample.com",
]
url_bloom = BloomFilter(urls)
print(url_bloom)

### 2. emails
emails = [
    "example1@example.com",
    "user2@test.org",
    "contact@mydomain.net",
    "admin@website.com",
    "info@anotherexample.com",
]
email_bloom = BloomFilter(emails)
print(email_bloom)

### 3. IP addresses
ip_addresses = [
    "192.168.0.1",
    "10.0.0.2",
    "172.16.0.3",
    "8.8.8.8",
    "127.0.0.1",
]
IP_bloom = BloomFilter(ip_addresses)
print(IP_bloom)

### 4. English words
english_words = [
    "apple",
    "banana",
    "cherry",
    "date",
    "elderberry",
    "fig",
    "grape",
    "honeydew",
    "kiwi",
    "lemon",
]
words_bloom = BloomFilter(english_words)
print(words_bloom)

### 5. DNA
dna_sequences = [
    "AGCTTAGCTA",
    "CGTAGCTAGC",
    "TGCATGCACT",
    "GCTAGCTAGC",
    "TAGCTAGCTA",
]
DNA_bloom = BloomFilter(dna_sequences)
print(DNA_bloom)

## Importing data with words of a short length
four_letter_words = [
    "bark", "clap", "dear", "echo", "fist", "gift", "hint", "jazz", "kite", "lamp",
    "mint", "nest", "pace", "quip", "rain", "snow", "toad", "urge", "vase", "warp",
    "arch", "bank", "dove", "flip", "gold", "hail", "jump", "leaf", "muse", "note"
]
four_letter_bloom = BloomFilter(four_letter_words)
print(four_letter_bloom)

#### Noted that all datasets are imported correctly


## Importing files with a lot of data from different file types

### 1. Txt file with words

words_dataset = []
with open("words.txt", 'r') as datafile:
    words_dataset = [line.strip() for line in datafile]

wordtxt_bloom = BloomFilter(words_dataset)
print(wordtxt_bloom)

### 2. Txt file with sequences

sequences_dataset = []
with open("sequences.txt", 'r') as datafile:
    sequences_dataset = [line.strip() for line in datafile]

sequences_bloom = BloomFilter(sequences_dataset)
print(sequences_bloom)

### 3. Csv file with a 1000 English words

english_words_dataset = []
with open("English_words.csv", 'r') as datafile:
    english_words_dataset = [line.strip() for line in datafile]

english_words_bloom = BloomFilter(english_words_dataset)
print(english_words_bloom)

### Noted that all the files are read correctly

# 2. Testing the result of the search function of the bloomfilter

## True postive

dna_sequences_test = [
    "AGCTTAGCTA",
    "CGTAGCTAGC",
    "TGCATGCACT",
    "GCTAGCTAGC"]

for word in dna_sequences_test:
    result = DNA_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

    

## False positive


## True negative

four_letter_words_test = [
    "bark", "test", "four", "unbelivehrdafkd", "fist", "gift", "hint", "jazz", "kite", "lamp",
    "mint", "nest", "pace", "quip", "rain", "snow", "toad", "urge", "vase", "warp",
    "arch", "bank", "dove", "flip", "gold", "hail", "jump", "leaf", "muse", "note"
]

for word in four_letter_words_test:
    result = four_letter_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

English_test = ["agony", "bread", "dad"]

for word in English_test:
    result = english_words_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

### Noted that all the words were correctly identified 
# as not in the four letter words bloom filter or the English test bloom filter.

## As expected, we did not find any false negatives in our testing.
