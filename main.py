from Target import Target
from Watchtower import Watchtower
from sklearn.metrics import classification_report
from classifier.SoundClassifier import *
from classifier.SoundDataManager import get_dataset_from_wavfile, get_train_test, pre_process
import pickle


def main():
    target = Target(40.4121, -86.94993)
    wt1 = Watchtower(40.41271, -86.9508, 80)
    wt2 = Watchtower(40.41301, -86.94991, 80)
    wt3 = Watchtower(40.41269, -86.94903, 80)


def get_trained_classifier(X_train, y_train, X_test, y_test, algorithm):
    X_test, X_train = pre_process(X_test, X_train)
    clf = SoundClassifier(algorithm)
    clf.train_classifier(X_train, y_train)
    predictions = clf.get_predictions(X_test)
    print(f"Accuracy Train =  {str(clf.get_accuracy(X_train, y_train))}")
    print(f"Accuracy Test  =  {str(clf.get_accuracy(X_test, y_test))}")
    print(classification_report(y_test, predictions))
    return clf


def train_classifier():
    # feature_type: 'mfcc' or 'filter_banks'
    data, target, filenames = get_dataset_from_wavfile('wavfiles/snap/', 'labels.csv', 1.5, 'mfcc', 'class1')
    X_test, X_train, y_test, y_train, train_index, test_index = get_train_test(data, target)
    X_test_processed, X_train_processed = pre_process(X_test, X_train)

    print("Final Report")
    clf = get_trained_classifier(X_train, y_train, X_test, y_test, "gnb")
    clf.get_predictions(X_test)
    # save
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)


if __name__ == '__main__':
    train_classifier()
