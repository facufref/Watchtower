from sklearn.metrics import classification_report
import pickle

from sklearn.metrics import classification_report

from classifier.SoundClassifier import *
from classifier.SoundDataManager import get_dataset_from_wavfile, get_train_test, get_dataset_from_array
from classifier.SoundRecorder import get_recording


def get_trained_classifier(X_train, y_train, X_test, y_test, algorithm):
    # X_test, X_train = pre_process(X_test, X_train)
    clf = SoundClassifier(algorithm)
    clf.train_classifier(X_train, y_train)
    predictions = clf.get_predictions(X_test)
    print(f"Accuracy Train =  {str(clf.get_accuracy(X_train, y_train))}")
    print(f"Accuracy Test  =  {str(clf.get_accuracy(X_test, y_test))}")
    print(classification_report(y_test, predictions))
    return clf


def train_classifier():
    # feature_type: 'mfcc' or 'filter_banks'
    data, target, filenames = get_dataset_from_wavfile('wavfiles/smalluav/', 'labels.csv', 1.5, 'mfcc', 'class1')
    X_test, X_train, y_test, y_train, train_index, test_index = get_train_test(data, target)

    print("Final Report")
    clf = get_trained_classifier(X_train, y_train, X_test, y_test, "gnb")
    # save
    with open('smalluav_v3_gnb_mfcc_clf_1-5sec.pkl', 'wb') as f:
        pickle.dump(clf, f)
    return clf


if __name__ == '__main__':
    clf = train_classifier()
    # recording = record()
    # prediction = clf.get_predictions(recording)
    # print(f'The prediction is {prediction}')
