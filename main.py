# %%
"""
PART 1

1. preprocess data - import and clean
    drop OpenInt
    create binary label and drop close

    for structure models:
        groupby week - group all days of week into one row, keep only full weeks (have 5 days)

Perceptron:
    2. Split train test, and X Y -
        80 - 20 (first 80% of days) # TODO make sure not split random
    3. Train perceptron on train
    4. predict perceptron on test
    5. show accuracy and graph

MEMM:
    Create list of lists (day features for each week)
    Add features - TODO
    Train Model
    Test Model
    show accuracy and graph

LSTM:
    Train Model
    Test Model
    show accuracy and graph


Compare results
"""
from sklearn.model_selection import train_test_split

from classifiers.LSTM import LSTM_phase
from classifiers.perceptron import perceptron_phase
from utils.params import TEST_SIZE, SHUFFLE_TRAIN_TEST
from utils.preprocessing import load_data
import matplotlib.pyplot as plt
import numpy as np
from pystruct.datasets import load_letters
from pystruct.models import ChainCRF
from pystruct.learners import StructuredPerceptron


def plots(df_day):
    df = df_day.copy()
    df = df.set_index(df_day['Date'])

    fig, axs = plt.subplots(1, 1)
    df['Open'].plot(ax=axs, title='IBM Stock Price, 1960 - 2020')
    axs.set_ylabel("Stock Price [USD]")

    plt.show()
    print(df_day.groupby(by='direction').count()['Date'])
    fig, axs = plt.subplots(1, 1)
    df_day.groupby(by='direction').count()['Date'].plot.bar(rot=0, ax=axs, title='Upward / Downward Days')
    axs.set_ylabel("Number of Days")
    axs.set_xticklabels(labels=['Down', 'Up'])

    plt.show()


def main():
    # load data
    df_day, week_features, week_targets = load_data(use_preloaded=False)

    # Plot Number of Upward / Downward days, and stock price
    # plots(df_day)

    # Perceptron
    perceptron_phase(df_day)

    ##PerceptronCRF
    PerceptronCRF(week_features, week_targets)

    # LSTM
    LSTM_phase(week_features, week_targets)



def PerceptronCRF(week_features, week_targets):
    print("------------- Structured Perceptron Phase -------------")
    X_train, X_test, y_train, y_test = train_test_split(week_features,
                                                        week_targets,
                                                        test_size=TEST_SIZE,
                                                        random_state=42,
                                                        shuffle=SHUFFLE_TRAIN_TEST)

    model = ChainCRF(directed=True)
    clf = StructuredPerceptron(model=model,average=200,verbose=1, max_iter=500)#,decay_exponent=0.9)
    clf.fit(X=X_train, Y=y_train.astype(int))
    print("Structured Perceptron Train Accuracy:", round(clf.score(X_train, y_train.astype(int)), 3))
    print("Structured Perceptron Test Accuracy:", round(clf.score(X_test, y_test.astype(int)), 3))
    plt.plot(clf.loss_curve_)
    plt.show()
    pass

if __name__ == '__main__':
    main()
