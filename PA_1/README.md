# Recommender Systems PA1

## Overview

### Description

The goal of this assignment is to implement a personalized collaborative movie recommender using either a memory-based or a model-based approach. As discussed in class, various implementation choices impact the quality of collaborative recommendations, including choices for data normalization, similarity computation, neighborhood selection, rating aggregation, and dimensionality reduction. As part of this assignment, you should try different instantiations of the aforementioned components, and verify the resulting recommendation performance of your implementation by submitting your produced recommendations to [Kaggle](https://www.kaggle.com/t/5fa9c6785e544f7faaaddcc9c6faf554).

### Evaluation

The evaluation metric for this assignment is Root Mean Squared Error (RMSE). The RMSE score, commonly used in the recommender systems literature, measures accuracy by penalizing prediction errors.

## Data

As stated in the specification document for this assignment, your implementation should be executed using the following command:

``` $ python3 main.py ratings.csv targets.csv > submission.csv ```

### File descriptions

You will need the following CSV files:

1. `ratings.csv`, containing historical ratings for 336,672 *<user, item>* pairs
2. `targets.csv`, containing the 77,276 *<user, item>* pairs for prediction

In addition, a sample `submission-rand.csv` file (with randomly assigned predictions) is provided for your convenience.

Note that each of these files contains a header line.

---


## Formulas
The matrix factorization in SVD is given by:

> R = T * &Sigma; * Q <sup>T<sup>

* R is a *u x i* (mxn) utility matrix;
* T is a *u x k* orthogonal left singular matrix, which represents the relationship between users and latent factors;
* &Sigma; is a *k x k* diagonal matrix, which describes the strength of each latent factor;
* Q is a *k x i* diagonal right singular matrix, which indicates the similarity between items and latent factors. 

### Prediction
Let each item be represented by a vector q<sub>i</sub> and each user is represented by a vector p<sub>u</sub>. The expected rating by a user on an item can be given as:

> ^r<sub>u,i</sub> =  p<sub>u</sub> * q<sup>T</sup><sub>i</sub>
> 
> ^r<sub>u,i</sub> =  &sum;<sup>k</sup><sub>f=1</sub> p<sub>u,f</sub> * q<sub>i,f</sub>

To minimize their RMSE we have:

> Min = (r<sub>u,i</sub> - &sum;<sup>k</sup><sub>f=1</sub> p<sub>u,f</sub> * q<sub>i,f</sub>)<sup>2</sup>
### Bias

* For a pair (u,i), &mu; is the average of all items
	* b<sub>i</sub> is the average rating of item i minus &mu;
	* b<sub>u</sub> is the average rating of user u minus &mu;

## Links

#### SVD
1. [reco](https://github.com/mayukh18/reco)
1. [Netflix Update: Try This at Home by Simon Funk](https://sifter.org/~simon/journal/20061211.html)
1. [Recommender system: Using singular value decomposition as a matrix factorization approach by Robin Witte](https://robinwitte.com/wp-content/uploads/2019/10/RecommenderSystem.pdf)
1. [Netflix Prize and SVD by Stephen Gower](http://buzzard.ups.edu/courses/2014spring/420projects/math420-UPS-spring-2014-gower-netflix-SVD.pdf)

#### General
1. [Formulas in Markdown](https://stackoverflow.com/questions/11256433/how-to-show-math-equations-in-general-githubs-markdownnot-githubs-blog)
2. [Greek Letters Symbols](https://www.keynotesupport.com/internet/special-characters-greek-letters-symbols.shtml)
3. [Other Punctuation](https://sites.psu.edu/symbolcodes/codehtml/#math)
