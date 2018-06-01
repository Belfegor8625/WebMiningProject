import nltk
import random
import pickle
from nltk import pos_tag
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC
import SentimentAnalisis.prep_data as prep

nltk.download('stopwords')


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


def make_tags_unique(documents):
    tmp_doc = []
    for text, tags in documents:
        try:
            tup = (text, tags[0])
        except IndexError:
            print(text)
            continue
        tmp_doc.append(tup)
    return tmp_doc


def make_tags_unique2(documents):
    tmp_doc = []
    for text, tags in documents:
        try:
            for tag in tags:
                tup = (text, tag)
                tmp_doc.append(tup)
        except IndexError:
            print(text)
            continue
    return tmp_doc


documents = prep.parse_xml_for_title_with_post_and_tag('Posts.xml')
tags = prep.parse_xml_for_tags_and_count('Tags.xml')

random.shuffle(documents)
print(documents[1])

word_features = list(tags.keys())


def remove_irrelevant_words(documents):
    new_documents = []
    for text, tags in documents:
        shorted_text = []
        for w_pos in nltk.pos_tag(text):
            if w_pos[1] in {'NN', 'NNS', 'WDP', 'WP', 'WP$', 'WRB', 'NNP', 'NNPS'}:
                shorted_text.append(w_pos[0])
        tup = (shorted_text, tags)
        new_documents.append(tup)
    return new_documents


documents = make_tags_unique(documents)
documents = remove_irrelevant_words(documents)
print(documents[1])
print(nltk.pos_tag(documents[1][0]))
featuresets = [(find_features(rev), category) for (rev, category) in documents]
print(featuresets.__len__())
train_part = round(featuresets.__len__() * 0.8)
training_set = featuresets[:train_part]
testing_set = featuresets[train_part:]
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:",
      (nltk.classify.accuracy(SGDClassifier_classifier, testing_set)) * 100)

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set)) * 100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
classifier.show_most_informative_features(10)
save_classifier = open("naivebayes.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()
