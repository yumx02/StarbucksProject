
# import necesary libraries
import pandas as pd
import numpy as np
import sys
import math
import json
from sqlalchemy import create_engine


## Datasets
'''
portfolio.json
* id (string) - offer id
* offer_type (string) - type of offer ie BOGO, discount, informational
* difficulty (int) - minimum required spend to complete an offer
* reward (int) - reward given for completing an offer
* duration (int) - time for offer to be open, in days
* channels (list of strings)

profile.json
* age (int) - age of the customer
* became_member_on (int) - date when customer created an app account
* gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
* id (str) - customer id
* income (float) - customer's income

transcript.json
* event (str) - record description (ie transaction, offer received, offer viewed, etc.)
* person (str) - customer id
* time (int) - time in hours since start of test. The data begins at time t=0
* value - (dict of strings) - either an offer id or transaction amount depending on the record
'''


# read in the json files
def load_data(portfolio_filepath, profile_filepath, transcript_filepath):
    portfolio = pd.read_json(portfolio_filepath, orient='records', lines=True)
    profile = pd.read_json(profile_filepath, orient='records', lines=True)
    transcript = pd.read_json(transcript_filepath, orient='records', lines=True)

    return portfolio, profile, transcript


def clean_portfolio(portfolio):
    '''
    IMPUT
    - portfolio(df): with columns below
        channels(list), difficulty(int),duration(int),id(str),
        offer_type(str),reward(int)
    OUTPUT
    - pf(df): with columns below
        mobile(0/1),email(0/1),web(0/1),social(0/1),
        offer_type(str),difficulty(int),reward(int),duration(int),
        offer_id(str)
    DESCRIPTION
    '''
    pf = portfolio
    web=[]
    email=[]
    mobile=[]
    social=[]
    channel = [[web,"web"],[email,"email"],[mobile,"mobile"],[social,"social"]]

    # transform channel column to each columns(web,email,mobile,social) with 0 or 1.
    for lt, col_name in channel:
        for x in pf["channels"]:
            if (col_name in x):
                lt.append(1)
            else:
                lt.append(0)
        pf[col_name] = lt    # append new colum to the dataframe

    # remain necessary columns
    pf = pf.loc[:, ["mobile","email","web","social","offer_type","difficulty","reward","duration","id"]]

    # arrange the appearance
    pf = pf.sort_values(['offer_type','difficulty'],ascending=[True, False]) #sort by offer_type and difficulty
    pf = pf.reset_index().drop("index",axis=1) #reset index
    portfolio = pf.rename(columns={'id': 'offer_id'}) #rename column to adjust to other DataFrames

    return portfolio



def clean_profile(profile):
    '''
    IMPUT
    - profile(df): with colums of gender(str),age(int),id(str),became_member_on(str),income(int)
    OUTPUT
    - profile(df): with colums of gender(str),age(int),person_id(str),became_member_on(str),income(int)
    DESCRIPTION
    - delete lows with age 118
    - change the column name from id to person_id
    - change the became_member_on(int) to became_member(date)
    '''
    profile = profile[profile["age"] != 118]
    profile = profile.rename(columns={'id': 'person_id'})


    # transform became_member_on(int) to became_member_year(int)
    year_list = []
    for date_int in profile["became_member_on"]:
        year = int(str(date_int)[:4])
        year_list.append(year)
    profile["became_member_year"] = year_list
    profile = profile.drop("became_member_on",axis=1)

    return profile



def clean_transcript(transcript):
    '''
    INPUT
        transcript(df): with colums of event(str),person(str),time(int),value(dict)
    OUTPUT
        tr_transaction(df): with colums below
            person_id(str),time(int),amount(float)
        tr_offer(df): with colums below
            person_id(str),time(int),offer_id(str),received(1/0),viewed(1/0),completed(1/0)
    DESCRIPTION
    - rename the column "person" to "person_id"
    - create two dataframe
        - the data which event is transaction
        - the data which event is offer(received, viewed, completed)
    '''

    # rename the column
    transcript = transcript.rename(columns={'person': 'person_id'})

    # 1. create transaction DataFrame ("event" == transaction)
    tr_transaction = transcript[transcript["event"]=="transaction"]

    ## clean tr_tranaction
    tr = tr_transaction
    amount = []
    for x in tr["value"]:
        if ("amount" in x):
            amount.append(x["amount"])
        else:
            amount.append(0)

    tr["amount"] = amount
    tr_transaction = tr.drop(["value","event"], axis=1)


    # 2. create offer DataFrame ("event" != transaction)
    tr_received = transcript[transcript["event"]=="offer received"]
    tr_viewed = transcript[transcript["event"]=="offer viewed"]
    tr_completed = transcript[transcript["event"]=="offer completed"]
    tr_offer = pd.concat([tr_received,tr_viewed,tr_completed])

    ## clean tr_offer
    tr = tr_offer
    offer_id = []
    for x in tr["value"]:
        if ('offer id' in x):
            offer_id.append(x['offer id'])
        elif ('offer_id' in x):
            offer_id.append(x['offer_id'])
        else:
            offer_id.append(0)

    tr["offer_id"] = offer_id
    tr = tr.drop("value", axis=1)

    ## offer events to each column
    viewed=[]
    received=[]
    completed=[]
    events = [[viewed,"viewed"],[received,"received"],[completed,"completed"]]

    for lt, col_name in events:
        for x in tr["event"]:
            if (col_name in x):
                lt.append(1)
            else:
                lt.append(0)
        tr[col_name] = lt

    tr_offer = tr.drop("event", axis=1).loc[:, ["person_id","time","offer_id","received","viewed","completed"]]
    tr_offer = tr_offer.rename(columns={'id': 'person_id'})

    return tr_transaction, tr_offer



def save_data(portfolio, profile, tr_transaction, tr_offer):
    '''save data
    INPUT:
    portfolio(df), profile(df), tr_transaction(df), tr_offer(df)

    Description:
    save the data for database
    '''

    engine = create_engine('sqlite:///data/clean_data.db')
    portfolio.to_sql('portfolio', engine, index=False)
    profile.to_sql('profile', engine, index=False)
    tr_transaction.to_sql('tr_transaction', engine, index=False)
    tr_offer.to_sql('tr_offer', engine, index=False)


def main():
    if len(sys.argv) == 4:

        portfolio_filepath, profile_filepath, transcript_filepath = sys.argv[1:]

        print('Loading data...\n    portfolio: {}\n    profile: {}\n    transcript: {}'
              .format(portfolio_filepath, profile_filepath, transcript_filepath))
        portfolio, profile, transcript = load_data(portfolio_filepath, profile_filepath, transcript_filepath)

        print('Cleaning data...')
        portfolio = clean_portfolio(portfolio)
        profile = clean_profile(profile)
        tr_transaction, tr_offer = clean_transcript(transcript)

        print('Saving data...')
        save_data(portfolio, profile, tr_transaction, tr_offer)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
