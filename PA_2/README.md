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

## Links
