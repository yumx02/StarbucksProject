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

'''
# load data
engine = create_engine('sqlite:///data/clean_data.db')

portfolio = pd.read_sql_table('portfolio', engine)
profile = pd.read_sql_table('profile', engine)
tr_transaction = pd.read_sql_table('tr_transaction', engine)
tr_offer = pd.read_sql_table('tr_offer', engine)
'''

# load data
def load_data(estimate_data_path):
    '''load data
    INPUT:
    estimate_data_path - csv file path of data for estimation.
    OUTPUT:
    estimate_data
    Description:
    load csv file and store it with pd dataframes
    '''
    estimate_data = pd.read_csv('data_to_estimate/estimate_data.csv')

    return estimate_data

# load model
model = pickle.load(open('model/classifier.pkl', 'rb'))

# use model to predict classification for query
### classification_labels = model.predict([query])[0]

def main():
    if len(sys.argv) == 2:
        estimate_data_path = sys.argv[1:]

        estimate_data = load_data(estimate_data_path)
        print("--------------")
        print("Estimate data")
        print(estimate_data)

        y_pred = model.predict(estimate_data)
        y_pred = pd.DataFrame(data=y_pred, columns=['success','fail','no_cont','no_int'])
        print("--------------")
        print("Estimate result")
        print(y_pred)


    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')

if __name__ == '__main__':
    main()
