import pandas as pd
import numpy as np
import sys
import math
import json
import sklearn
import pickle
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



model = pickle.load(open('../model/classifier.pkl', 'rb'))

# use model to predict classification for query
def main(imput_data):
    '''
    if len(sys.argv) == 2:
        estimate_data_path = sys.argv[1:]

        estimate_data = load_data(estimate_data_path)
    '''
    estimate_data = imput_data
    print("--------------")
    print("Estimate data")
    print(estimate_data)

    y_pred = model.predict(estimate_data)
    y_pred = pd.DataFrame(data=y_pred, columns=['success','fail','no_cont','no_int'])
    print("--------------")
    print("Estimate result")
    print(y_pred)

    return y_pred
