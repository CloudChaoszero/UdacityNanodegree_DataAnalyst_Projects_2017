# P5-ML-Enron-Analysis

## File Directory

1. Reports
	a. [Main Report (CONDENSED)](Analysis/Reports_PDF/Enron_POI_Report_CONDENSED.pdf)
	b. [Main Report: Documenation](Analysis/Reports_PDF/Enron_POI_Report.pdf)

	c. [Analysis: Documenation](Analysis/Reports_PDF/Eron_Email_MainAnalysis.pdf)

2. Code
	a. [Main Report: Write-Up](Analysis/Analysis-Final/Enron-POI-Final Report.ipynb)

	b. [Analysis: Code](Analysis/Analysis-Cleaning-Code/"P5-Enron-Email-Cleaning-and-Analysis.ipynb")

3. Additional Resources

	a. [Images](Images/)

	b. [Prepared Data for Analysis](Output-Files/)

	c. [Supplementary Files](Supplementary-Files/)


## Overview


### Objective

We utilize several Machine Learning techniques from an Enron employee email and financial information dataset from the 2001 time period. 

The goal of this project is to find some N amount of features to sufficiently predict POI in some fraudulent scenario.

### Background

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud.

In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives. 

![Enron Image](./Images/Enron.jpg)


In this project, we will play detective, and put our new skills to use by building a person of interest identifier based on financial and email data made public as a result of the Enron scandal. 
To assist us in our detective work, Udacity had combined this data with a hand-generated list of persons of interest in the fraud case, which means individuals who were indicted, reached a settlement or plea deal with the government, or testified in exchange for prosecution immunity.




### Concepts Used

1. Machine Learning
	
	a. Decision Trees

	b. GridSearchCV

	c. Pipeline

	d. Extra Trees

	e. SVM(Standard Vector Machine)



# Conclusion and Remarks

# Question 1
<span style="color:purple">_Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those? _ </style>
___

### Overview
This project provided partially conclusive findings of suspected Enron employees in the 2002 Enron fraudlent scenario, **Person of Interest(POI)**, by using machine learning techniques.

> We define POI  as someone who was indictedor settled in the case without admitting guilt. We utilized several techniques to come closer to answering the previously mentioned goal.

### The Data 

The dataset we operated on was JSON formatted information on Enron employee financial statuses and email interactions. These features were integral in answering our question from the following reasoning:

- Financial information is a central theme around industry corruption. For example, [Martin Shkreli heavily increased the price of a drug from $/$ $13.50 to $/$ $750.00.](https://www.scientificamerican.com/article/martin-shkreli-who-raised-drug-prices-from-13-50-to-750-arrested-in-securities-fraud-probe/) This action was from the fact that several drug companies implement the same methodology for profitability.

- Communicating with a corrupt individual quite often is an indicator of aiding in abetting. 

To solve for POI concerns, we turned to machine learning algorithms for identifying corruption with our financial and email information. A classical approach in machine learning is e-mail classification from logistic regression within supervised learning. However, we implemented two other supervised learning algorithms to determine Enron POI.

However, to implement these algorithms, we inspected the data for:

1. Misinformation (typos)

2. Lack of information (Null values)

3. Obscure information (outliers)

### Handling Outliers and more

Using the inter-quartile range, we removed obscure data from our analysis and imputated some information. 

> We removed outlier entries such as "TOTAL" and two other entries due to "NaN" or absurd information recorded. This removal of infectious data enabled us to proceed with the analysis in better fashion than before.

In the case of removing outliers, I just set some condition for extracting/neglecting outlier information as we update the dataset.

In the case of imputing data, I created a function to replace existing "NaN" values with the integer "0." Thereafter, we verified the changes in our introductory data analysis of Salary versus Bonus.
___

## Question 2

<span style="color:purple">_What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values._</span>

We select several numerical features. Moreoever, we factor in the four engineered features, seen in the following subsection

> We will implement four new features to potentially indentify Eron POI. 

> The **first two** additions are the ratio between an employee and the CEO, _Jeffrey K. Skilling_.

> The implementation for these four new features can lead to the following:

> - If the ratio in bonus between an employee and the CEO is significantly closer to the value 1, then we can suspect some type of corruption occuring.

> - If the ratio in salary between an employee and the CEO is significantly closer to the value 1, then we can suspect some type of corruption occuring.

> These features are linear transformations of the salary and bonus information presented. We factor how close ones's financial information is with respect to the CEO to determine POI relationship.

> The **remaining two** additional features are the inbound and outbound email ratios between a POI.


> The implementation for these four new features can lead to the following:

> - If the ratio $\dfrac{\text{Received emails from POI}}{\text{All received Emails}}$ is closer to the value 1, we can suspect an individual is a POI.

> - If the ratio $\dfrac{\text{Sent emails from POI}}{\text{All Sent Emails}}$ is closer to the value 1, we can suspect an individual is a POI.

We then implemented a few algorithms to decide on what top three to four features we should implement for predicting people of interest in the Enron email scandal.

I.e. we zoom out to consider the following features, then zoom in to precise feature selections to predict Enron fraudsters.

1. POI

2. CEO to Employee Bonus Ratio

3. Total Payments

4. Exercised Stock Options

5. CEO to Employee Salary Ratio

6. Restricted Stock

7. Shared Receipt with POI

8. FROM POI to This Person

9. From Messages

10. From this Person to POI

11. Ratio of Sent Messages to POI

12. Ratio of Received Messages to POI

13. Deferral Payments

14. Loan Advances

15. Restricted Stock Deferred
                 
16. Deferred Income

17. Expenses

18. Other

19. Long Term Incentive

20. Director Fees

> <a style = "color:red">Note:</a> **We do not** implement Salary and Bonus into our feature selection process due to the multicollinearity association to CEO to Employee Salary Ratio and CEO to Employee Bonus Ratio, respectively. Moreover, "From Poi to this Person," "From Messages", and "From this Person to Poi" are collinear with ratio of interactions with POI

> **Cutoff Criteria:** We select the top features of each algorithm implementation with a cutoff score being a a 5 digit difference between two sequential features (e.g. Total expenses being .10 and the next being 0.05) [SelectK best case: 5.0+ digit difference.]. 

Thereafter, we proceeeded through three iterations of a _feature selection_ process, where each case utilized a different algorithm. 


**Feature Selection with SKBest Procedure**

We implement the [SelectKBest](http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html) method for selecting features according to the **k** highest scores. These k factors will be one of our few considerations for feature selection.

> Added: Per correction/comment, 'k' looks at the features after score computation and keeps the top features for next fitting process.

The following are the ranked features with the parameter **k**='all':

![SelectKBest Ranking Features](../../Images/RankedFeat_SelectKBest.jpg)

we observe that CEO to Employee Bonus Ratio and CEO to Employee Salary Ratio ranked within top 5 features for our model selection, as seen below:

1. Exercised Stock Options

2. Total Stock Value

3. CEO To Employee Salary Ratio

4. CEO To Employee Bonus Ratio

5. Total Payments

**Feature Selection with Extra Trees Implementation**


The Extra Trees classifier is a variant of the popular Random Forest algorithm. However, each step of the Extra Trees implementation has random decision boundaries selected, rather than the best one. Moreover, Extra Trees classifier is great for our numerical features.

The following are the ranked features with no altered parameters, default parameters.

![Extra Trees Ranking Features](../../Images/RankedFeat_ExtraTrees.jpg)

Our findings within the Extra Trees implementation had Exercised Stock Options  as our top feature recommendation.


**Feature Selection with Decision Tree Algorithm**

Decision tree builds classification or regression models in the form of a tree structure. It breaks down a dataset into smaller and smaller subsets while at the same time an associated decision tree is incrementally developed. The final result is a tree with decision nodes and leaf nodes.

The following are the ranked features with no altered parameters, default parameters.

![Extra Trees Ranking Features](../../Images/RankedFeat_DT.jpg)

For ranking the importance of all recommended features, The top important features are:

1. Total Stock Value

2. CEO to Employee Bonus Ratio

3. Expenses

Our top features only have one commmon feature in common from the results of our other features. This feature is CEO to Employee Bonus Ratio.

Moreover, this scenario has a precision of 0.20 and recall of 0.40 for determining POI. This is partially good to see, however we should observe that this, and the past outcomes, is not optimal for model implementation. I.e.,Notice that we implemented the Decision Tree algorithm with default parameters, and previous algorithms as well. This consideration occurs because we do not know if our feature selection process was optimal in selection. 

### Feature Selection: Final Decision


The top re-occuring features to select from where, in frequency:

1. CEO To Employee Bonus Ratio

2. CEO To Employee Salary Ratio

3. Exercised Stock Options

Additionally, we include two additionaly engineered features:

4. ratio_of_received_messages_to_poi

5. ratio_of_sent_messages_to_poi



___


___

## Question 3

<span style="color:purple">_What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?_</span>

We implemented SelectKbest, Extra Trees, and Decision Tree algorithm for obtaining an optimal feature count for model fitting and ranking features to best classify POI of Enron employees.


Thereafter, we compared and contrasted between Gaussian Naive Baye's algorithm and Decision Tree implementions to best predict POI.

The following are the results from the Gaussian Naive Baye's implementation:

![Gaussian Naive Baye's Results](../../Images/Tuning_GNB1.jpg)

![Gaussian Naive Baye's Results](../../Images/Tuning_GNB2.jpg)


This process took 8.8seconds from a total of 1600 fits. We had a recommendation of priors being "None" for the Naive Baye's Implementation. The resulting model performance from this recommendation of hypertuning was a precision of 33%, recall of 20%, and an accuracy of ~84%. 

This is somewhat acceptable. we now turn to the Decision Tree implemenation to hopefully obtain more desirable results.

The following are the results from the Decision Tree's implementation:

![Gaussian Naive Baye's Results](../../Images/Tuning_DT1.jpg)

![Gaussian Naive Baye's Results](../../Images/Tuning_DT3.jpg)

This process took 1.8minutes from a total of 16200 fits. We had parameter recommendations of: 

1. class_weight=None
2. criterion='gini'
3. max_depth=5,
4. max_features=None
5. max_leaf_nodes=None
6. min_impurity_split=1e-07
7. min_samples_leaf=7
8. min_samples_split=8
9. min_weight_fraction_leaf=0.04
10. splitter='best'

for the Naive Baye's Implementation. 

The resulting model performance from this recommendation of hypertuning was a precision of 67%, recall of 40%, and an accuracy of ~89.74%. 

Though we sacrificed time in the Decision Tree implementation, we obtained better results than that of the Gaussian Naive Baye's algorithm. Therefore, we proceeded into our analysis with the Decision Tree implementation.

___

## Question 4

<span style="color:purple">_What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune?_</span>

Tuning parameters for an algorithm is a rigorous attempt at finding some optimal factors/identifiers to best create a statistical forecast model. If you we failed to reject or even disvalue the importance of tuning, we fail to find the a both precise and accurate model for future cases outside some past observations.

We obtained several model performance results from Gaussian Baive Baye's Implementation in the following:

| Metrics |  Gaussian Naive Bayes Algorithm Time before Tuning(seconds)  |Accuracy before Tuning|Precision Before Tuning|Recall before Tuning|F1-Score before Tuning|Gaussian Naive Bayes Algorithm Time after Tuning (seconds) |Accuracy after Tuning|Precision after Tuning|Recall after Tuning|F1-Score after Tuning|
|--------|--------|--------|--------|--------|--------|--------|--------|------|------|----|
|  Default Settings | 0.005| 0.846| 0.33| 0.20| 0.25| **0.005**| **0.846**| **0.33**| **0.20**| **0.25**|
|Non-POI 90% | 0.005| 0.846| 0.33| 0.20| 0.25| **0.002**| **0.128**|**0.13**| **1.00**| **0.23**|
|Non-POI 60%| 0.005| 0.846| 0.33| 0.20| 0.25| **0.001**| **0.795**| **0.20**| **0.20**| **0.20**|
|Non-POI 10% | 0.005| 0.846| 0.33| 0.20| 0.25| **0.001**| **0.846**|** .33**| **0.20 **|**0.25**|

We observe the Gaussian Naive Bayes implementation is best with default settings, or prior probability of Non-POI at/around 10%.


We utilized the Decision Tree algorithm. Other algorithms utilized were Extra Trees and Select K Best. The perfomance from each model were quick. However, the results were inconsistent and mixed up. Moreover, there were faults to each scenario. However, the Decision Tree worked more favorable with obtaining optimal features for our logistic problem.

The following is outputs for Decision Tree Implementation with manual tuning:

| Metrics |  Decision Tree Algorithm Time before Tuning(seconds)  |Accuracy before Tuning|Precision Before Tuning|Recall before Tuning|F1-Score before Tuning| Decision Tree Algorithm Time after Tuning (seconds) |Accuracy after Tuning|Precision after Tuning|Recall after Tuning|F1-Score after Tuning|
|--------|--------|--------|--------|--------|--------|--------|--------|------|------|----|
|  Default Settings | 0.003| 0.821| 0.33| 0.40| 0.36| **0.003**| **0.821**| **0.33**| **0.40**| **0.36**|
|min_weight_fraction_leaf=0.0001 | 0.003| 0.821| 0.33| 0.40| 0.36| **0.002**| **0.821**|**0.33**| **0.40**| **0.36**|
|min_samples_split=3| 0.003| 0.821| 0.33| 0.40| 0.36| **0.001**| **0.8210**| **0.33**| **0.40**| **0.36**|
|min_samples_leaf=5 | 0.003| 0.821| 0.33| 0.40| 0.36| **0.002**| **0.8462**|** .33**| **0.20 **|**0.25**|
|max_depth = 7 | 0.003| 0.821| 0.33| 0.40| 0.36| **0.001**| **0.821**| **0.33**| **0.40**| **0.36**|

Everything highlighted in bold, the latter five columns are different parameters being tuned. The firt five columns are the default Decision Tree Algorithm model output.

Recalling that our Decision Tree implementation was a more ideal approach for model optimization, we utilized the Decision Tree implementation we tuned the following parameters:

1. max_depth

2. max_leaf_nodes

3. min_samples_leaf

4. min_samples_split

5. min_weight_fraction_leaf


We selected these factors based on computation and processing speed. If we had a better computing system (#IWishIhadCloudComputing) our tuning could have been more broad and deep.

The following details is our implemenation of hypertuning with Pipeline and GridSearchCV implemenation.

From the tester tuning these parameters, they can
1. Evaluated our data faster
2. Confirmed Optimal Accuracy

Utilizing the Pipeline and GridSearchCV libraries, the following code provided

fitting 1000 folds for each of 432 candidates, totalling 432000 fits, as seen below

> Pipeline(steps=[('kbest', SelectKBest(k='all', score_func=\<function f_classif at 0x00000000099DB518>)), 

> ('dtree', DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=3,

> max_features=None, max_leaf_nodes=None,

> min_impurity_split=1e-07, min_samples_leaf=5,

> min_samples_split=7, min_weight_fraction_leaf=0.001,

> presort=False, random_state=None, splitter='best'))])

Again we see, utilizing the recommended parameters and feature_list features that we manually selected, we receive the following output from tester.py:

![Tester python file](../../Images/tester.jpg)

We have recall and precision scores of .30+. Moreover, our accuracy is ~0.86%!


___

## Question 5

<span style="color:purple">What is validation, and what’s a classic mistake you can make if you do it wrong?</span>

Validation is referred to as the process where a trained model is evaluated with a testing data set. With this partitioning of data, validation serves a purpose of using the testing data to test a trained model for generalizations. We test our trained model's precision, accuracy, and recall rates. 

One classic mistake if you can do it wrong is incorrectly guessing future cases in which affect production/company performance. This incorrect predictions are commonly due to overfitting or underfitting the model shaped by the training data.

> A brief analogy of improper fitting for predictions can be guessing your time of arrival of meeting a friend. You usually take a path for 15minutes, and therefore tell this person. However, you take the busy street adjacent to the path you usually take, and become 3minutes late, due to traffice. The model was predicting your time of arrival from inputs like exprience crossing street and pace you travel. This is an example of **overfitting.**

## Question 6 

<span style="color:purple">_Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. [relevant rubric item: “usage of evaluation metrics”]_</span>



Fitting 100 folds for each of 162 candidates, totalling 16200 fits, as seen below

> Pipeline(steps=[('kbest', SelectKBest(k='all', score_func=\<function f_classif at 0x00000000099DB518>)), 

> ('dtree', DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=3,

> max_features=None, max_leaf_nodes=None,

> min_impurity_split=1e-07, min_samples_leaf=5,

> min_samples_split=7, min_weight_fraction_leaf=0.001,

> presort=False, random_state=None, splitter='best'))])

Utilizing the recommended parameters and feature_list features that we manually selected, we receive the following output from tester.py:

![Tester python file](../../Images/tester.jpg)

We have recall and precision scores of .30+. Moreover, our accuracy is ~0.86!

> Note: When TP < FP, then accuracy will always increase when we change a classification rule to always output “negative” category. Conversely, when TN < FN, the same will happen when we change our rule to always output “positive
> This following section also provides the Precision, Recall, and F1-Score related to our implemented models. 

> In our case,

>**Precision** (TP)/(TP+FP) cares about whether the positive examples predicted by our model were correct. In our case, what's the % Enron employees classified as POI correctly out of all classified Enron Employees classified as POI.

>**Recall** (TP)/(TP+FN) cares more on whether we have predicted all positive examples in the data. In our case, what is the percent of predictions were correctly identified POI, for all actual POI.


>where TP:=True Postive, FN:=False Negative, FP:= False Postives, TN:= True Negatives, as seen below



| True State/Diagnosis | NOT POI | POI |
|---------------------:|---------|-----|
|              NOT POI | TN      | FP  |
|                  POI | FN      | TP  |


    
    
## Remarks

**Quick Recap**

- We dealt with with an imperfect, real-world dataset

- We validated a machine learning result using test data

- We evaluated a machine learning result using quantitative metrics

- We created, select and transform features

- We hypter tuned machine learning algorithms for maximum performance

**Interesting Fact**

- Testing data is a high variance outcome. In future cases, we should be concerned with overfitting or underfitting, for the sake of abiding to the variance contraint from testing data.


**Comparing Cross-Validation with Train/Test splits:**

- Cross Validation:

     + More accurate estimate for out-of-sample accuracy

    + more efficient use of data
    
- Train/Test Split
    + Runs K times faster than K-fold cross validation
    + Simplier to exampled detailed results
    
**Feature Engineering**

- Our CEO Salary Bonus/Salary Ratios were collinear with Bonus and Salary, respectively. Therefore, we removed Bonus and Salary as feature considerations for our analysis. If we would have implemented these features, accuracy and other performance factors for predicting POI Enron Employees would have been heavily inflated.