#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import numpy as np
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from time import time

### FEATURE SELECTION 
# features_list is a list of strings, each of which is a feature name.
# the first feature must be "poi".
# there are 21 features available: 14 finanacial, 6 email, 1 for poi
# there are 146 names in the dataset
# there are 35 POIs in the dataset
# only 18 POIs are in the dataset though
full_features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 
                 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
                 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees', 
                 'to_messages', 'from_poi_to_this_person', 'from_messages', 
                 'from_this_person_to_poi', 'shared_receipt_with_poi', 'to_not_enron_messages']
features_list = ['poi', 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "rb"))

### REMOVE OUTLIERS
data_dict.pop("TOTAL", None)
#might not necessarily be an outlier but I don't think this should be considered a person
data_dict.pop("THE TRAVEL AGENCY IN THE PARK", None)

### CREATE NEW FEATURE
# new feature created from findNonEnron.py
# counts how many emails were sent to people with emails that didn't have enron in the domain
not_enron_dict = pickle.load(open("my_data.pkl", "rb"))
# prints out how many people in the dataset do not have value for new feature
missing_not_enron = 0
poi_missing_not_enron = 0
for person in data_dict.keys():
	try:
		data_dict[person]['to_not_enron_messages'] = not_enron_dict[data_dict[person]['email_address']]
	except KeyError:
		data_dict[person]['to_not_enron_messages'] = 'NaN'
		if data_dict[person]['poi'] == True:
			poi_missing_not_enron += 1
		else:
			missing_not_enron += 1
print("POIs missing new to_not_enron_messages feature:", poi_missing_not_enron)
print("Non-POI missing new to_not_enron_messages feature:", missing_not_enron)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)
labels = np.array(labels)
features = np.array(features)

### SCALE FINANCIAL FEATURES
from sklearn import preprocessing
#features = preprocessing.scale(features)

### CHOOSE A CLASSIFIER
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
dt = DecisionTreeClassifier()
nb = GaussianNB()
sv = SVC()
clf = dt

### TUNE PARAMETERS USING GRIDSEARCHCV
from sklearn.grid_search import GridSearchCV
#param_grid = {"criterion": ["gini", "entropy"], "min_samples_split": [2, 3, 4], "max_features": [1, 2, 3, 4]}
#clf = GridSearchCV(dt, param_grid = param_grid, scoring = 'recall')

# Dump your classifier, dataset, and features_list
dump_classifier_and_data(clf, my_dataset, features_list)

### VALIDATION
# test using StratifiedShuffleSplit
# same as tester.py
from sklearn.cross_validation import StratifiedShuffleSplit
sss = StratifiedShuffleSplit(labels, 1000, test_size = 0.1, random_state = 42)

total_labels = []
total_predictions = []
for train_index, test_index in sss:
	# Separate data into training and testing sets
	features_train, features_test = features[train_index], features[test_index]
	labels_train, labels_test = labels[train_index], labels[test_index]
	total_labels.extend(labels_test)
	
	# GridSearchCV separates SSS training set into training set and validation set
	# using 
	# selects best parameters for classifier from grid based on score from validation set
	clf = clf.fit(features_train, labels_train)
	#use classifier to predict whether person is POI or not on test set
	predictions = clf.predict(features_test)
	total_predictions.extend(predictions)

from sklearn.metrics import precision_recall_fscore_support
precision, recall, fscore, support = precision_recall_fscore_support(total_labels, total_predictions, 
	beta = 1, average = 'binary')

PERF_FORMAT_STRING = "Precision: {:06.5f} \nRecall: {:06.5f} \nfscore: {:06.5f}"
print(PERF_FORMAT_STRING.format(precision, recall ,fscore))
