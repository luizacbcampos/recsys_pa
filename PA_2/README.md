# Recommender Systems PA2: Content-based Movie Recommendation

## Overview

### Description

The goal of this assignment is to implement a content-based movie recommender by exploiting movie metadata obtained from [OMDB](http://omdbapi.com/). As discussed in class, various implementation choices impact the quality of content-based recommendations, including choices for content representation (e.g., unigrams, n-grams, concepts, named entities, latent topics), user profiling (e.g., by aggregating positive and negative feedback), and user-item similarity estimation. As part of this assignment, you should try different instantiations of these components, and verify the resulting recommendation performance of your implementation by submitting your produced recommendations to [Kaggle](https://www.kaggle.com/t/9f681ccc0e6c42a4b7a49e491f570a72).

### Evaluation:
The evaluation metric for this assignment is Root Mean Squared Error (RMSE). The RMSE score, commonly used in the recommender systems literature, measures accuracy by penalizing prediction errors.


## Data

As stated in the specification document for this assignment, your implementation should be executed using the following command:

``` $ python3 main.py content.csv ratings.csv targets.csv > submission.csv ```

### File descriptions
You will need the following CSV files:

- `content.csv`, containing 22,080 _<item, content>_ pairs
- `ratings.csv`, containing historical ratings for 336,672 _<user, item>_ pairs
- `targets.csv`, containing the 77,276 _<user, item>_ pairs for prediction

In addition, a sample `submission-rand.csv` file (with randomly assigned predictions) is provided for your convenience.

Note that each of these files contains a header line.

### Output
For each of the *<user, item>* pairs in the `targets.csv` input file, your implementation should predict the corresponding numeric rating, by leveraging the item metadata available from `content.csv` and the historical user-item matrix available from `ratings.csv`. 

**You must not use any historical information about the target item.**

The resulting prediction should be written to standard output as a *<user, item, rating>* tuple, formatted as two CSV columns:
- _UserId:ItemId_, containing the *<user, item>* pair separated by a colon (:)
- _Prediction_, containing the predicted rating for the target pair

## Grading policy
This assignment is worth a total of 15 points, with the possibility of attaining up to 5 extra points. These points are distributed as:
* 5 points for your documentation, assessed based on a short (pdf) report describing your implemented data structures and algorithms, their computational complexity, as well as a discussion of your attained results (e.g.,
based on the various submissions you uploaded to Kaggle).
* 5 points for your implementation, assessed based on the quality of your source code, including its overall organization (modularity, readability, indentation, use of comments) and appropriate use of data structures.
* 5 points for your performance, assessed based on the RMSE score of your last submission on Kaggle’s private leaderboard relative to the performance of your fellow contestants

## Eligibility

To be eligible for the performance grades, you must satisfy the following:
1. You must upload at least one submission to Kaggle within the timeframe of this assignment;
2. The source code that you submit (via Moodle) by the deadline should be able to precisely generate your last submission to Kaggle;
3. Your implementation should be able to execute correctly in a Linux environment under 5 minutes.

---

## Content-based Recommendation

### Description of the Content
In this approach, the user is suggested an item based on the description of the item.

**Tokenization**
1. Lower the string
1. Transforms numbers to words using [num2words](https://github.com/savoirfairelinux/num2words)
1. Stemming with Porter Stemmer or Snowball Stemmer (Porter2)

**Term Frequency-Inverse Document Frequency(TF-IDF)** TF-IDF is used in Information Retrieval for feature extraction purposes and it is a sub-area of Natural Language Processing(NLP). 

- _Term Frequency_: frequency of the word in the current document to the total number of words in the document. It signifies the occurrence of the word in a document and gives higher weight when the frequency is more so it is divided by document length to normalize.
  - ![\Large tf](https://latex.codecogs.com/svg.latex?TF%28f%29%20%3D%20%5Cfrac%7B%5Ctext%7BFrequency%20occurance%20of%20term%20t%20in%20document%7D%7D%7B%5Ctext%7BTotal%20number%20of%20terms%20in%20document%7D%7D)
  - TF<sub>ti</sub>: term frequency of term _t_ in item _i_;
  
- _Inverse Document Frequency_: total number of documents to the frequency occurrence of documents containing the word. It signifies the rarity of the word. It helps in giving a higher score to rare terms in the documents. 
  - ![\Large idf](https://latex.codecogs.com/svg.latex?IDF%28t%29%20%3D%20%5Clog%20%5Cleft%20%28%20%5Cfrac%7B%5Ctext%7BTotal%20number%20of%20documents%7D%7D%7B%5Ctext%7BNumber%20of%20documents%20containing%20term%20t%7D%7D%20%5Cright%20%29)
  - idf<sub>t</sub>: inverse document frequency of term _t_;

__TF\*IDF__: weight given to each term.



## Links

1. [Beginners Guide to learn about Content Based Recommender Engines](https://www.analyticsvidhya.com/blog/2015/08/beginners-guide-learn-content-based-recommender-systems/)
1. [Introduction to TWO approaches of Content-based Recommendation System](https://towardsdatascience.com/introduction-to-two-approaches-of-content-based-recommendation-system-fc797460c18c)
1. [Content-Based Recommendation System](https://medium.com/@bindhubalu/content-based-recommender-system-4db1b3de03e7)
1. [Content-based Recommender Systems: State of the Art and Trends](https://www.researchgate.net/publication/226098747_Content-based_Recommender_Systems_State_of_the_Art_and_Trends)
1. [Content-based Recommender System for Movie Website](https://www.diva-portal.org/smash/get/diva2:935353/FULLTEXT02.pdf)
1. [Porter Stemmer](https://tartarus.org/martin/PorterStemmer/)