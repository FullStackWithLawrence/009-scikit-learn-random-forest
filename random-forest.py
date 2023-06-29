# Encoding: utf-8
"""
    written by:     Lawrence McDaniel
                    https://lawrencemcdaniel.com

    date:           jun-2023

    usage:          minimalist implementation of Logistic Regression model.
"""
import os
import warnings

# ------------------------------------------------------------------------------
# IMPORTANT: DON'T FORGET TO INSTALL THESE LIBRARIES WITH pip
# ------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# module initializations
sns.set()
HERE = os.path.abspath(os.path.dirname(__file__))
warnings.filterwarnings("ignore")


def metrics_score(actual, predicted):
    """
    Create a common function for measuring the
    accuracy of both the train as well as test data.
    """
    print("Metrics Score.")
    print(classification_report(actual, predicted))

    cm = confusion_matrix(actual, predicted)
    plt.figure(figsize=(8, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt=".2f",
        xticklabels=["Not Cancelled", "Cancelled"],
        yticklabels=["Not Cancelled", "Cancelled"],
    )
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.show()


def prepare_data():
    """
    Raw database transformations:
        - clean the data
        - remove columns that don't contain any information
        - recast data types as necessary
        - convert categorical data into series of dummy columns
        - split dependent / independent variables
        - split training / test data sets
    """
    print("Preparing data sets")
    original_db = pd.read_csv(os.path.join(HERE, "data", "reservations-db.csv"))

    # need to be careful to only work with a **COPY** of the original
    # source data, lest we accidentally permanently modify any of this
    # raw data.
    data = original_db.copy()

    # remove the ID column from the data set, since it contains
    # no predictive information.
    data = data.drop(["Booking_ID"], axis=1)

    # recast dependent variable as boolean
    data["booking_status"] = data["booking_status"].apply(
        lambda x: 1 if x == "Canceled" else 0
    )

    # hive off the dependent variable, "booking_status"
    x = data.drop(["booking_status"], axis=1)
    y = data["booking_status"]

    # encode all categorical features
    x = pd.get_dummies(x, drop_first=True)

    # Split data in train and test sets
    return train_test_split(x, y, test_size=0.30, stratify=y, random_state=1)


def random_forest():
    """
    - create training and test data sets
    - create a Logistic Regression model
    - train the model
    - generate confusion matrix and f-score for the training set
    - generate confusion matrix and f-score for the test set
    """
    print("Random Forest")
    x_train, x_test, y_train, y_test = prepare_data()

    print("- training")
    rf_estimator = RandomForestClassifier(
        class_weight={0: 0.17, 1: 0.83}, random_state=1
    )
    rf_estimator.fit(x_train, y_train)

    print("- modeling on training data")
    y_pred_train_rf = rf_estimator.predict(x_train)
    metrics_score(y_train, y_pred_train_rf)

    print("- modeling on test data")
    y_pred_test_rf = rf_estimator.predict(x_test)
    metrics_score(y_test, y_pred_test_rf)


if __name__ == "__main__":
    random_forest()
