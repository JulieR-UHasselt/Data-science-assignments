This folder is used for the project of the course 'Concepts of Data Science DL'.
This project is done by Julie Robbrecht and Shadi Hamdan.
The purpose of the project is to implement a bloom filter.

# document the content of the repository
#reference to the files to add

# summary of your conclusions
We chose to implement the bloom filter using a functional approach.

# source of datasets:
- words.txt: https://github.com/dwyl/english-words?tab=readme-ov-file
- sequences.txt: https://github.com/MuhammadShan7/genome
# Conclusion_ performance test
The Bloom Filter performance test successfully processed a dataset of 466,550 English words from words.txt. Over 10 runs, the creation time averaged around 16.9 seconds, with memory usage consistently at approximately 35.775 MB. The average search time remained extremely fast at 0.000008 seconds per query. The false positive rate varied between 0.40% and 1.50%, indicating the Bloom Filter's effectiveness in maintaining a low rate of incorrect positive identifications.

It is important to note that these numbers are not fixed and may vary slightly with each execution. The results presented here are an example from one particular trial with the words.txt dataset. Re-running the tests multiple times and averaging the results can provide a more stable and accurate measure of the Bloom Filter's performance.
