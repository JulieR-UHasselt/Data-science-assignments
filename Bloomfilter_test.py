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
url_bloom = BloomFilter(urls,  P=0.1) #note that we change the P value to performance false negative testing
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

## Importing files with a lot of data from different file types

### 1. Txt file with words

words_dataset = []
with open("English_words.txt", 'r') as datafile:
    words_dataset = [line.strip() for line in datafile]

wordtxt_bloom = BloomFilter(words_dataset, P=0.1) #note that we change the P value to performance false negative testing
print(wordtxt_bloom)

### 2. Txt file with sequences

sequences_dataset = []
with open("sequences.txt", 'r') as datafile:
    sequences_dataset = [line.strip() for line in datafile]

sequencestxt_bloom = BloomFilter(sequences_dataset)
print(sequencestxt_bloom)

### 3. Csv file with a 1000 English words

english_words_dataset = []
with open("English_words.csv", 'r') as datafile:
    english_words_dataset = [line.strip() for line in datafile]

english_words_csv_bloom = BloomFilter(english_words_dataset)
print(english_words_csv_bloom)


# Testing the result of the search function of the bloomfilter

## 1. True postive

dna_sequences_test = [
    "AGCTTAGCTA",
    "CGTAGCTAGC",
    "TGCATGCACT",
    "GCTAGCTAGC"]

for word in dna_sequences_test:
    result = DNA_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

sequences_test = [
"CGTATCTTCGTGTGCTCTCCTTTAGAACTGCATCTCTAGAGTCAGAGAGG",
"AGAGCATTGTATCCGACCGAACTCCTGTAGTGACAAAACCGTCCTCAATG",
"TCGACCGAACTCCCTGCCTCTCATCGCGGATCACGTCCGCCGAGATAATA"]

for word in sequences_test:
    result = sequencestxt_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

## 2. False positive

wordtxt_bloom_test = [
    "bark", "test", "four", "unbelivehrdafkd", "fist", "gift", "hint", "jazz", "kite", "lamp",
    "mint", "nest", "pace", "quip", "rain", "snow", "toad", "urge", "vase", "warp",
    "arch", "bank", "dove", "flip", "gold", "hail", "jump", "leaf", "muse", "note"
]

for word in wordtxt_bloom_test:
    result = wordtxt_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

## 3. True negative

url_bloom_test = [
    "https://www.bbc.com/",
    "https://www.twitter.com/",
    "https://www.youtube.com/",
    "https://www.amazon.com/",
    "https://www.google.com/",
    "https://www.khanacademy.org/",
    "https://www.theverge.com/",
    "https://www.webmd.com/",
    "https://www.booking.com/",
    "https://www.imdb.com/"
]

for word in url_bloom_test:
    result = url_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")

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
    result = english_words_csv_bloom.search_bit_array(word)
    print(f"Word '{word}' found: {result}")
