#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pickle
import time 

from sklearn import cross_validation
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest

from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','ratio_of_received_messages_to_poi', 'ceo_to_employee_bonus_ratio','ratio_of_sent_messages_to_poi'
                 ,'ceo_to_employee_salary_ratio','exercised_stock_options']
### Load the dictionary containing the dataset
with open("../Output-Files/my_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

data = featureFormat(data_dict, features_list)


### split into labels and features 
labels, features = targetFeatureSplit(data)


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
sss = cross_validation.StratifiedShuffleSplit(labels, n_iter=1000,test_size = 0.30, random_state=11)


for i_train, i_test in sss:
    features_train, features_test = [features[i] for i in i_train], [features[i] for i in i_test]
    labels_train, labels_test = [labels[i] for i in i_train], [labels[i] for i in i_test]

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
# ##### Naive Bayes Algorithm with Manual Tuning Cases
# 
# Naive Bayes is a classification technique based on Bayes’ Theorem with an assumption of independence among predictors. More information can be found in my [Machine Learning Basics Documenation](https://github.com/CloudChaoszero/General-Statistics-and-ML-Concepts/blob/master/ML/Machine_Learning_Notes.ipynb).
# 
# The following are several manual tuning cases for the Naive Bayes implementation. In each scenario, we modify the following classifier's parameter:
# 
# 1. Prior
#     
#     > Note: Priors are the probabilities of the classes. If specified the priors are not adjusted according to the data.

# In[67]:

from sklearn.naive_bayes import GaussianNB

def GNB_hypertuning(priors):
    #Modified Parameters
    
    #Start Timer
    t0 = time.time()
    clf = GaussianNB(priors)
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    print("Manual Tuning Decision tree algorithm time in %0.3fs" % (time.time() - t0))

    acc= metrics.accuracy_score(labels_test, pred)
    print "Tuning Accuracy: ", acc

    # function for calculation ratio of true positives
    # out of all positives (true + false)
    print 'Manual Tuning Precision: ', metrics.precision_score(labels_test,pred)

    # function for calculation ratio of true positives
    # out of true positives and false negatives
    print 'Manual Tuning Recall: ', metrics.recall_score(labels_test,pred)
    print(classification_report( labels_test,pred))


# ###### Gaussian Naive Bayes Manual Tuning with Default Settings

# In[68]:

GNB_1 = GNB_hypertuning(priors = None)


# ###### Gaussian Naive Bayes Manual Tuning with Prior Probability Not POI at 90%

# In[69]:

GNB_2 = GNB_hypertuning(priors = [.1,.9])


# ###### Gaussian Naive Bayes Manual Tuning with Prior Probability Not POI at 60%

# In[70]:

GNB_3 = GNB_hypertuning(priors = [.4,.6])


# ###### Gaussian Naive Bayes Manual Tuning with Prior Probability Not POI at 10%

# In[71]:

GNB_4 = GNB_hypertuning(priors = [.9,.1])


# | Metrics |  Gaussian Naive Bayes Algorithm Time before Tuning(seconds)  |Accuracy before Tuning|Precision Before Tuning|Recall before Tuning|F1-Score before Tuning|Gaussian Naive Bayes Algorithm Time after Tuning (seconds) |Accuracy after Tuning|Precision after Tuning|Recall after Tuning|F1-Score after Tuning|
# |--------|--------|--------|--------|--------|--------|--------|--------|------|------|----|
# |  Default Settings | 0.005| 0.846| 0.33| 0.20| 0.25| **0.005**| **0.846**| **0.33**| **0.20**| **0.25**|
# |Non-POI 90% | 0.005| 0.846| 0.33| 0.20| 0.25| **0.002**| **0.128**|**0.13**| **1.00**| **0.23**|
# |Non-POI 60%| 0.005| 0.846| 0.33| 0.20| 0.25| **0.001**| **0.795**| **0.20**| **0.20**| **0.20**|
# |Non-POI 10% | 0.005| 0.846| 0.33| 0.20| 0.25| **0.001**| **0.846**|** .33**| **0.20 **|**0.25**|
# 
# We observe the Gaussian Naive Bayes implementation is best with default settings, or prior probability of Non-POI at/around 10%.

# ##### Decision Tree Algorithm with Manual tuning Cases
# 
# The following are several manual Hypertuning cases of the Decision Tree Classifier. In each scenario, we modify the following classifier's parameters:
# 
# 1. Max Depth
# 
# 2. Min Samples Split
# 
# 3. Min Samples Leaf 
# 
# 4. Min Weight Fraction Leaf

# In[72]:

def DTA_hyperTuning(max_depth, min_samples_split, min_samples_leaf, 
                    min_weight_fraction_leaf):    
    #Modified Parameters
    ## use manual tuning parameter min_samples_split
    
    #Start Timer
    t0 = time.time()
    clf = DecisionTreeClassifier(max_depth = max_depth, min_samples_split=min_samples_split, 
                                      min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf)
    clf = clf.fit(features_train,labels_train)
    pred= clf.predict(features_test)
    print("Manual Tuning Decision tree algorithm time in %0.3fs" % (time.time() - t0))

    acc= metrics.accuracy_score(labels_test, pred)
    print "Tuning Accuracy: ", acc

    # function for calculation ratio of true positives
    # out of all positives (true + false)
    print 'Manual Tuning Precision: ', metrics.precision_score(labels_test,pred)

    # function for calculation ratio of true positives
    # out of true positives and false negatives
    print 'Manual Tuning Recall: ', metrics.recall_score(labels_test,pred)
    print(classification_report( labels_test,pred))


# ###### Decision Tree Algorithm with Default Settings

# In[73]:

DTA_1 = DTA_hyperTuning(max_depth = None, min_samples_split=2, min_samples_leaf=1, 
                    min_weight_fraction_leaf=0)


# ###### Decision Tree Algorithm with Min Weight Fraction Leaf Parameter altered

# In[74]:

DTA_2 = DTA_hyperTuning(max_depth = None, min_samples_split=2, min_samples_leaf=1, 
                    min_weight_fraction_leaf=0.0001)


# ###### Decision Tree Algorithm with Min Sample Split Parameter Altered

# In[75]:

DTA_3 = DTA_hyperTuning(max_depth = None, min_samples_split=3, min_samples_leaf=1, 
                    min_weight_fraction_leaf=0)


# ###### Decision Tree Algorithm with Min Sample Leaf Parameter Altered

# In[76]:

DTA_4 = DTA_hyperTuning(max_depth = None, min_samples_split=2, min_samples_leaf=5, 
                    min_weight_fraction_leaf=0)


# In[77]:

DTA_5 = DTA_hyperTuning(max_depth = 7, min_samples_split=2, min_samples_leaf=1, 
                    min_weight_fraction_leaf=0)


# We have tuned several parameters for obtaining the best accurate, precise, and good recall model, manually. Below is a summary recap of our manual tuning.

# | Metrics |  Decision Tree Algorithm Time before Tuning(seconds)  |Accuracy before Tuning|Precision Before Tuning|Recall before Tuning|F1-Score before Tuning| Decision Tree Algorithm Time after Tuning (seconds) |Accuracy after Tuning|Precision after Tuning|Recall after Tuning|F1-Score after Tuning|
# |--------|--------|--------|--------|--------|--------|--------|--------|------|------|----|
# |  Default Settings | 0.003| 0.821| 0.33| 0.40| 0.36| **0.003**| **0.821**| **0.33**| **0.40**| **0.36**|
# |min_weight_fraction_leaf=0.0001 | 0.003| 0.821| 0.33| 0.40| 0.36| **0.002**| **0.821**|**0.33**| **0.40**| **0.36**|
# |min_samples_split=3| 0.003| 0.821| 0.33| 0.40| 0.36| **0.001**| **0.8210**| **0.33**| **0.40**| **0.36**|
# |min_samples_leaf=5 | 0.003| 0.821| 0.33| 0.40| 0.36| **0.002**| **0.8462**|** .33**| **0.20 **|**0.25**|
# |max_depth = 7 | 0.003| 0.821| 0.33| 0.40| 0.36| **0.001**| **0.821**| **0.33**| **0.40**| **0.36**|



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Gaussian Naive Baye HyperTuning

# In[79]:

folds = 100
kbest = SelectKBest()

# A stratified shuffle split is used here to counter the effects of the class imbalance problem
sss = StratifiedShuffleSplit(labels, folds, random_state = 11)

# We could initially test a default decision tree classifier.  The tree could be fine-tuned as well.
gnb = GaussianNB()

# A pipeline is used to chain the SelectKBest and Decision Tree
pipeline = Pipeline([('kbest', kbest), ('gnb', gnb)])
param_grid = {'kbest__k':['all',2,3,5],'gnb__priors':[None,[.1,.9],[.9,.1],[.5,.5]]}
grid_search = GridSearchCV(estimator = pipeline, 
                           param_grid = param_grid,
                           scoring = 'f1',
                           cv = sss,
                           verbose = 1)
grid_search.fit(features, labels)
clf = grid_search.best_estimator_
print(clf)


# Our results show that the Gaussian Naive Bayes Classifier parameters should be tuned to the following value:
# 
# 1. Priors: None

# In[80]:

GNB_hypertuning(None)


# Decision Tree HyperTuning

# In[81]:

folds = 100
kbest = SelectKBest()

# A stratified shuffle split is used here to counter the effects of the class imbalance problem
sss = StratifiedShuffleSplit(labels, folds, random_state = 11)

# We could initially test a default decision tree classifier.  The tree could be fine-tuned as well.
dtree = DecisionTreeClassifier()

# A pipeline is used to chain the SelectKBest and Decision Tree
pipeline = Pipeline([('kbest', kbest), ('dtree', dtree)])
param_grid = {'kbest__k':['all',3],'dtree__min_samples_split':[6,7,8],'dtree__max_depth':[3,4,5],
             'dtree__min_samples_leaf':[3,5],'dtree__min_samples_leaf':[5,6,7],'dtree__min_weight_fraction_leaf':[0.001,0.02,0.04]}
grid_search = GridSearchCV(estimator = pipeline, 
                           param_grid = param_grid,
                           scoring = 'f1',
                           cv = sss,
                           verbose = 1)
grid_search.fit(features, labels)
clf = grid_search.best_estimator_
print(clf)


# Our results show that the Decision Tree Classifier parameters should be tuned to the following values:
# 
# - class_weight=None
# - criterion='gini'
# - max_depth=5,
# - max_features=None
# - max_leaf_nodes=None
# - min_impurity_split=1e-07
# - min_samples_leaf=7
# - min_samples_split=8 
# - min_weight_fraction_leaf=0.04
# - splitter='best'
# 
# Comparing the two models, we observe that the Decision Tree Classifier brings in a .20 increase in precision for classiying POI, compared to the Gaussian Naive Bayes implementation. 
# ##### Validating the Decision Tree Algorithm with Hypertuning 
# 
# We validate how well our Decision Tree Algorithm performed with HyperTuning.  

# In[86]:

t0 = time.time()

clf_DTC1 = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=5,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=5,
            min_samples_split=6, min_weight_fraction_leaf=0.02,
            presort=False, random_state=None, splitter='best')
clf_DTC1.fit(features_train,labels_train)
pred_decisionTree = clf_DTC1.predict(features_test)
score = clf_DTC1.score(features_test,labels_test)
print 'Accuracy before tuning: ', score
decTree_precision_1 = metrics.precision_score(pred_decisionTree,labels_test)
decTree_recall_1 = metrics.recall_score(pred_decisionTree,labels_test)
print 'Precision before tuning: ', decTree_precision_1
print 'Recall before tuning: ', decTree_recall_1
print "Decision tree algorithm time:", round(time.time()-t0, 3), "s"

# Example starting point. Try investigating other evaluation techniques!

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf_DTC1, my_dataset, features_list)