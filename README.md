# QuranSearchByTopic
This Project is developed to help all Muslims to deal with the Holy Quran easier and faster. as this Project allow them to search the
Quran for specific Keyword or Verse, and also for a Concrete Topic or Conceptual Topic and to help them in it's Memorization and Recitation also [See Recitation Part](https://github.com/EyadMShokry/QuranSearchAndMemorization).

This project consists of two parts; the first is a Search Engine based on a Deep Learning Model called 'word2vec' used to search in the
Quran using Keyword, Verse or Topic with accuracy about 70%.
[The second part](https://github.com/EyadMShokry/QuranSearchAndMemorization) is an iOS Application, which used to introduce the first part, which we mentioned and, also, to help users memorize and recite the Quran using Voice and help them know their mistakes. This system has high accuracy in Evaluating users' sayings in comparison of other applications.

It is a Search Engine for Quran written in Python that allows you to search by Topic or Concept like صلة الرحم, الميراث.
our Search Engine is not only matching the words, but it uses a Deep Learning Model called word2vec, or Word-To-Vector to take into consideration the meaning/semantic of the words. Download it [from here](https://drive.google.com/openid=1xGfrpibTLlqMdmil9hCW2__QDkv9M7nQ)

## Dataset Preparation
we needed to get a documented and trusted representation of verses of the whole Quran and their according topics, Because this is something religious which we cannot make it ourselves to be trusted for the users of the application.

### Mushaf Al Tajweed Quran book
- Author: compiled by Dr. Mohammed Fayez Kamel Under Supervision of Dr. Ali Abu Al-Kheir.
- Publisher: published by Dar Al-Maarifa in Syria and authenticated by Al Azhar Islamic Research Academy in Egypt
You can see online version from it [here](https://ar.islamway.net/book/23758/%D9%85%D8%B5%D8%AD%D9%81-%D9%85%D8%B9%D9%84%D9%85-%D8%A7%D9%84%D8%AA%D8%AC%D9%88%D9%8A%D8%AF-%D9%85%D8%B9-%D9%85%D9%84%D8%AD%D9%82-%D8%A7%D9%84%D9%85%D8%B9%D8%AC%D9%85-%D8%A7%D9%84%D9%85%D9%81%D9%87%D8%B1%D8%B3-%D9%84%D9%85%D9%88%D8%A7%D8%B6%D9%8A%D8%B9-%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86-%D8%A7%D9%84%D9%83%D8%B1%D9%8A%D9%85)

We used this book to annotate each verse with it's related topic. So we could map each User's Query to the most related Topic using our word2vec model and Cosine Similarity technique. Then retrive the verses of this topic.

## Word2Vec Model
### Arabic Islamic Corpus for training the Model
We collected our Corpus which we used to train the word2vec model from many resources:
- [Quran Text](http://tanzil.net) with total number 751,291 words
- [Watan-2004](https://sites.google.com/site/mouradabbas9/corpora) Abbas et al., 2011 with total number of 106,289,288 words
- CNN-arabic, (Saad and Ashour, 2010) OSAC: Open Source Arabic Corpus with total number of 23,984,550 words
- BBC-arabic, (Saad and Ashour, 2010) OSAC: Open Source Arabic Corpus with total number of 19,833,141 words
- [Arabic Book Reviews](http://www.mohamedaly.info/datasets/labr) Aly and  Atiya, 2013 LABR: Large Scale Arabic Book Reviews with total number of 38,065,922 words
- [Hadith dataset](https://www.kaggle.com/fahd09/hadith-dataset/version/1) with 2,410,569 words and 34,409 unique words
- The Islamic folder of [KSUCCA Dataset](https://mahaalrabiah.wordpress.com/2012/07/20/king-saud-university-corpus-of-classical-arabic-ksucca/) with total number 23,645,087 words

### Training the Model
We collected all of this corpora in only one txt file and after processing it we used it to train our word2vec model using this command:
`$ ./word2vec -train corpus.txt -output model.bin -cbow 1 -size 300 -window 10 -threads 8 -binary 1 -iter 15`

**Note**: This is not the final version of the Project. It's still under Development.
