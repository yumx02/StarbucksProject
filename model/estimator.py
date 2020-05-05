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


def load_data():
    '''load data
    INPUT:
    database_filepath - database with  id, message, original, genre,
                        and 36 categories(related, request...etc) columns.
    OUTPUT:
    X - pd.DataFrame of messages
    Y - pd.DataFrame of genre and 36 categories(related, request...etc)
    Description:
    load database which created by process_data.py
    '''
    engine = create_engine('sqlite:///data/clean_data.db')
    portfolio = pd.read_sql_table('portfolio', 'sqlite:///data/clean_data.db')
    profile = pd.read_sql_table('profile', 'sqlite:///data/clean_data.db')
    tr_transaction = pd.read_sql_table('tr_transaction', 'sqlite:///data/clean_data.db')
    tr_offer = pd.read_sql_table('tr_offer', 'sqlite:///data/clean_data.db')
    return portfolio, profile, tr_transaction, tr_offer


def offer_result(tr_offer):
    '''
    INPUT
        tr_offer(df): with colums below
            person_id(str),time(int),offer_id(str),received(1/0),viewed(1/0),completed(1/0)
    OUTPUT
        df_result(df): with colums below
            person_id(str),offer_id(str),time(int),received(1/0),viewed(1/0),completed(1/0),
            success(1/0),fail(1/0),no_cont(1/0),no_int(1/0)
    DESCRIPTION
    - create four columns: success, fail, no_cont, and no_int
    - sort by time
    '''
    df_prep = tr_offer.groupby(["person_id","offer_id"]).sum()

    df_prep["success"] = 0
    df_prep["fail"] = 0
    df_prep["no_cont"] = 0
    df_prep["no_int"] = 0

    df_success = df_prep[(df_prep["viewed"]>0) & (df_prep["completed"]>0)]
    df_success["success"] = 1

    df_fail = df_prep[(df_prep["viewed"]>0) & (df_prep["completed"]==0)]
    df_fail["fail"] = 1

    df_no_cont = df_prep[(df_prep["viewed"]==0) & (df_prep["completed"]>0)]
    df_no_cont["no_cont"] = 1

    df_no_int = df_prep[(df_prep["viewed"]==0) & (df_prep["completed"]==0)]
    df_no_int["no_int"] = 1

    df_result = pd.concat([df_success, df_fail, df_no_cont, df_no_int])
    df_result = df_result.sort_values("time")
    df_result = df_result.reset_index()

    return df_result



def pf_prep(portfolio):
    '''
    INPUT
        portfolio(df): with colums below
            mobile(0/1),email(0/1),web(0/1),social(0/1),offer_type(str),
            difficulty(int),reward(int),duration(int), offer_id(str)
    OUTPUT
        pf_prep(df): with colums below
            mobile(0/1),email(0/1),web(0/1),social(0/1),
            difficulty(int),reward(int),duration(int), offer_id(str),
            bogo(0/1),discount(0/1),info(0/1)

    DESCRIPTION
    - replace offer_type column to each column(bogo,discount,info)
    '''
    bogo=[]
    discount=[]
    info=[]

    pf_prep = portfolio
    promo = [[bogo,"bogo"],[discount,"discount"],[info,"info"]]

    for lt, col_name in promo:
        for x in pf_prep["offer_type"]:
            if (col_name in x):
                lt.append(1)
            else:
                lt.append(0)
        pf_prep[col_name] = lt

    pf_prep = pf_prep.drop("offer_type", axis=1)

    return pf_prep



def profile_prep(pf_profile):
    '''
    INPUT
        profile(df): with colums below
            gender(str),age(int),person_id(str),became_member_on(str),income(int)
    OUTPUT
        pf_profile(df): with colums below
            age(int),person_id(str),income(int),became_member_year(int),M(0/1),F(0/1),O(0/1)
    DESCRIPTION
    - replace gender column to each column(M,F,O)
    - transform became_member_on(str) to became_member_year(int)
    '''
    M=[]
    F=[]
    O=[]

    gender = [[M,"M"],[F,"F"],[O,"O"]]

    for lt, col_name in gender:
        for x in pf_profile["gender"]:
            if (col_name in x):
                lt.append(1)
            else:
                lt.append(0)
        pf_profile[col_name] = lt

    pf_profile = pf_profile.drop("gender", axis=1)

    return pf_profile



def df_prep(tr_offer_prep, pf_prep, profile_prep):
    '''
    INPUT
        tr_offer_prep(df): with colums below
            person_id(str),offer_id(str),time(int),received(1/0),viewed(1/0),completed(1/0),
            success(1/0),fail(1/0),no_cont(1/0),no_int(1/0)
        pf_prep(df): with colums below
            mobile(0/1),email(0/1),web(0/1),social(0/1),
            difficulty(int),reward(int),duration(int), offer_id(str),
            bogo(0/1),discount(0/1),info(0/1)
        pf_profile(df): with colums below
            age(int),person_id(str),income(int),became_member_year(int),M(0/1),F(0/1),O(0/1)
    OUTPUT
        df_prep(df): with colums below
            time(int),success(0/1),fail(0/1),no_cont(0/1),no_int(0/1),
            mobile(0/1),email(0/1),web(0/1),social(0/1),
            difficulty(int),reward(int),duration(int),bogo(0/1),discount(0/1),info(0/1),
            age(int),income(int),became_member_year(int),M(0/1),F(0/1),O(0/1)
    DESCRIPTION
    - replace gender column to each column(M,F,O)
    - transform became_member_on(str) to became_member_year(int)
    '''
    df_prep = pd.merge(tr_offer_prep, pf_prep ,on="offer_id")
    df_prep = pd.merge(df_prep, profile_prep ,on="person_id")

    df_prep = df_prep.drop(["received","viewed","completed"],axis=1)
    df_prep = df_prep.drop(["person_id","offer_id"],axis=1)

    return df_prep



def create_test_train(df_prep, num_test = 5000):
    '''
    INPUT
        df_prep(df): with colums below
        num_test(int): the number of test data. the rest of data become train data.
   　OUTPUT
        X_train(df),X_test(df): colums below
            mobile(0/1),email(0/1),web(0/1),social(0/1),
            difficulty(int),reward(int),duration(int),bogo(0/1),discount(0/1),info(0/1),
            age(int),income(int),became_member_year(int),M(0/1),F(0/1),O(0/1)
        Y_train(df),Y_test(df):columns below
            success(0/1),fail(0/1),no_cont(0/1),no_int(0/1)
    DESCRIPTION
    - devide into X_train,Y_train,X_test,Y_test dataset
    - test dataset includes 'nun_test' numbers of rows, and the rest of the data is in train.
    '''
    df1 = df_prep.sort_values("time")
    df1 = df1.reset_index().drop(["index","time"], axis=1)

    X = df1.drop(["success","fail","no_cont","no_int"],axis=1)
    Y = df1.loc[:,["success","fail","no_cont","no_int"]]

    num_train = df1.shape[0] -num_test

    X_train = X.head(num_train)
    X_test = X.tail(num_test)

    Y_train = Y.head(num_train)
    Y_test = Y.tail(num_test)

    return X_train, Y_train, X_test, Y_test


def build_model(X_train, Y_train):
    #Decide on some random forest parameter candidates
    parameters = {
        'n_estimators' :[3,5,10,30,50],#Number of decision trees to create
        'random_state' :[7,42],
        'max_depth' :[3,5,8,10,30],#Decision tree depth
        'min_samples_leaf': [2,5,10,20,50],#Minimum number of samples of the node that has finished branching
        'min_samples_split': [2,5,10,20,50]#Number of samples required when the decision tree branches
        }
    #Use grid search
    from sklearn.model_selection import GridSearchCV
    clf = GridSearchCV(estimator=RandomForestClassifier(), param_grid=parameters, cv=2, iid=False)

    return clf



def evaluate_model(clf, X_test, Y_test):
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(Y_test, y_pred)
    print('Accuracy: {}'.format(accuracy))



def save_model(clf, model_filepath):
    '''save model
    INPUT:
    model - model to be pickled
    model_filepath -path to save the model
    Description:
    save the model as a pickle at the specified path.
    '''
    with open(model_filepath, 'wb') as f:
        pickle.dump(clf, f)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))

        portfolio, profile, tr_transaction, tr_offer = load_data()

        tr_offer_prep = offer_result(tr_offer)
        portfolio_prep = pf_prep(portfolio)
        profiles_prep = profile_prep(profile)

        df_preparation = df_prep(tr_offer_prep, portfolio_prep, profiles_prep)
        X_train, Y_train, X_test, Y_test = create_test_train(df_preparation)



        print('Building model...')
        clf = build_model(X_train, Y_train)


        print('Training model...')
        clf.fit(X_train, Y_train)
        clf.best_params_

        print('Evaluating model...')
        evaluate_model(clf, X_test, Y_test)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(clf, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
