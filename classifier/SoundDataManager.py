import pyparsing
from classifier.SoundProcessor import get_processed_mfcc, get_processed_filter_banks
from scipy.io import wavfile
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
import math


def get_train_test(data, target):
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
    for train_index, test_index in split.split(data, target):
        X_train, X_test = data[train_index], data[test_index]
        y_train, y_test = target[train_index], target[test_index]
    return X_test, X_train, y_test, y_train, train_index, test_index


def get_dataset_from_wavfile(root, file_name, chunk_size_in_seconds, feature_type, class_column):
    df = pd.read_csv(root + file_name)
    data, target, filenames = get_data_target_filenames(df, root, chunk_size_in_seconds, feature_type, class_column)
    return data, target, filenames


def get_dataset_from_array(sample_rate, signal, chunk_size_in_seconds):
    list_mfcc = []
    # signal = stereo_to_mono(signal)
    mfcc_list = get_processed_mfcc(sample_rate, signal, chunk_size_in_seconds)
    for mfcc in mfcc_list:
        flattened_mfcc = mfcc.flatten()
        list_mfcc.append(flattened_mfcc)
    data = np.vstack(list_mfcc)
    return data


def get_data_target_filenames(df, root, chunk_size_in_seconds, feature_type, class_column):
    list_mfcc = []
    filenames = []
    target = []
    df.set_index('fname', inplace=True)
    for f in df.index:
        file = wavfile.read(root + f)
        sample_rate, signal = file
        # signal = stereo_to_mono(signal)

        if feature_type == 'mfcc':
            mfcc_list = get_processed_mfcc(sample_rate, signal, chunk_size_in_seconds)
        elif feature_type == 'filter_banks':
            mfcc_list = get_processed_filter_banks(sample_rate, signal, chunk_size_in_seconds)
        else:
            raise Exception(f'No feature type with value {feature_type}')

        for mfcc in mfcc_list:
            file_class = get_dataframe_first_match(df, f, class_column)
            if file_class == 'null':
                continue
            flattened_mfcc = mfcc.flatten()
            list_mfcc.append(flattened_mfcc)
            filenames.append(f)
            target.append([file_class])
    data = np.vstack(list_mfcc)
    return data, np.array(target), filenames


def pre_process(X_test, X_train):
    """One way to pre process I found on "Introduction to machine learning with Python: a guide for data scientists." Chapter 2
        There must be a better way to do this"""
    # compute the mean value per feature on the training set
    mean_on_train = X_train.mean(axis=0)
    # compute the standard deviation of each feature on the training set
    std_on_train = X_train.std(axis=0)
    # subtract the mean, scale by inverse standard deviation
    # afterwards, mean=0 and std=1
    X_train_scaled = (X_train - mean_on_train) / std_on_train
    # use THE SAME transformation (using training mean and std) on the test set
    X_test_scaled = (X_test - mean_on_train) / std_on_train
    return X_test_scaled, X_train_scaled


def get_dataframe_first_match(df, row, column):
    match = df.loc[row, column]
    if isinstance(match, pyparsing.basestring):
        return match
    match = 'null' if math.isnan(match) else match.iat[0]
    return match


def stereo_to_mono(signal):
    if signal.ndim == 2:
        return signal[:, 0]/2 + signal[:, 1]/2
    return signal
