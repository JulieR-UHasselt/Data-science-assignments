from Bloomfilter import Bloom_Filter


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
url_bloom = Bloom_Filter(urls)
print(url_bloom)

### 2. emails
emails = [
    "example1@example.com",
    "user2@test.org",
    "contact@mydomain.net",
    "admin@website.com",
    "info@anotherexample.com",
]
email_bloom = Bloom_Filter(emails)
print(email_bloom)

### 3. IP addresses
ip_addresses = [
    "192.168.0.1",
    "10.0.0.2",
    "172.16.0.3",
    "8.8.8.8",
    "127.0.0.1",
]
IP_bloom = Bloom_Filter(ip_addresses)
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
words_bloom = Bloom_Filter(english_words)
print(words_bloom)

### 5. DNA
dna_sequences = [
    "AGCTTAGCTA",
    "CGTAGCTAGC",
    "TGCATGCACT",
    "GCTAGCTAGC",
    "TAGCTAGCTA",
]
DNA_bloom = Bloom_Filter(dna_sequences)
print(DNA_bloom)

#### Noted that all datasets are imported correctly


## Importing data with words of a short length
four_letter_words = [
    "bark", "clap", "dear", "echo", "fist", "gift", "hint", "jazz", "kite", "lamp",
    "mint", "nest", "pace", "quip", "rain", "snow", "toad", "urge", "vase", "warp",
    "arch", "bank", "dove", "flip", "gold", "hail", "jump", "leaf", "muse", "note"
]
four_letter_bloom = Bloom_Filter(four_letter_words)
print(four_letter_bloom)


## Importing files with a lot of data from different file types

### 1. Txt file with words

words_dataset = []
with open("words.txt", 'r') as datafile:
    words_dataset = [line.strip() for line in datafile]

wordtxt_bloom = Bloom_Filter(words_dataset)


