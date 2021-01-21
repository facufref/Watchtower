from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class SoundClassifier:
    def __init__(self, algorithm):
        if algorithm == 'knn':
            self._classifier = KNeighborsClassifier(n_neighbors=6)
        elif algorithm == 'linear':
            self._classifier = LogisticRegression()  # alternative => (C=100) / (C=0.01)
        elif algorithm == 'linearMulti':
            self._classifier = LinearSVC()
        elif algorithm == 'decisionTree':
            self._classifier = DecisionTreeClassifier(random_state=0)  # alternative => max_depth=4
        elif algorithm == 'randomForest':
            self._classifier = RandomForestClassifier(n_estimators=1000, max_features=1300, max_depth=8, random_state=0)
        elif algorithm == 'gradientBoosting':
            self._classifier = GradientBoostingClassifier(random_state=0)  # alternative => max_depth=1, learning_rate=0.01
        elif algorithm == 'svm':
            self._classifier = SVC()  # alternative => C=1000, gamma=1000. Also pre-process data
        elif algorithm == 'neuralNetworks':
            self._classifier = MLPClassifier(random_state=0)  # alternative => max_iter=1000, alpha=1. Also pre-process data
        else:
            print('Algorithm not found')

    def train_classifier(self, X_train, y_train):
        self._classifier.fit(X_train, y_train)

    def get_predictions(self, X_test):
        return self._classifier.predict(X_test)

    def get_accuracy(self, X_test, y_test):
        return self._classifier.score(X_test, y_test)


def print_predictions(predictions, filenames, test_index):
    for i in range(0, len(predictions)):
        print(f" The file '{filenames[test_index[i]]} is {str(predictions[i])}")