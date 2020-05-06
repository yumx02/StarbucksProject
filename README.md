# Disaster Response Pipeline Project
### Project Overview
- create a machine learning pipeline to categorize disaster messages so that you can send the messages to an appropriate disaster relief agency.
- An original data set, which is from Figure Eight(https://appen.com/), contains real messages that were sent during disaster events.
- project includes:
    - a web app where an emergency worker can input a new message and get classification results in several categories.
    - figures which display visualizations of the data.

![screenshot of web app](https://github.com/yumx02/DisasterResponsePipeline/blob/master/Screen%20Shot%202020-04-20%20at%2021.54.35.png)

### Project Components
1. ETL Pipeline
    - In process_data.py, write a data cleaning pipeline that:
        - Loads the messages and categories datasets
        - Merges the two datasets
        - Cleans the data
        - Stores it in a SQLite database

2. ML Pipeline
    - In train_classifier.py, write a machine learning pipeline that:
        - Loads data from the SQLite database
        - Splits the dataset into training and test sets
        - Builds a text processing and machine learning pipeline
        - Trains and tunes a model using GridSearchCV
        - Outputs results on the test set
        - Exports the final model as a pickle file

3. Flask Web App
    - Flask web app to visualize the results using Plotly.


### File Structure
  ┣━ app  
  ┃    ┣━ run.py - Flask application  
  ┃    ┗━ templates  
  ┃        ┣━ go.html - web application of classification result.  
  ┃        ┗━ master.html - web application of master page.  
  ┣━ data  
  ┃    ┣━ disaster_categories.csv - dataset of disaster categories.  
  ┃    ┣━ disaster_messages.csv - dataset of disaster messages.  
  ┃    ┣━ process_data.py - data processing script.  
  ┃    ┗━ DisasterResponse.db - database of cleaned data.  
  ┣━ models  
  ┃    ┣━ train_classifier.py - NLP and ML pipeline script.  
  ┃    ┗━ classifier.pkl - pickle file of classifier  
  ┗━ README.md - this file  

<<<<<<< HEAD
||||||| merged common ancestors
### Table of Content
1. [Project Overview](#project_overview)
1. [Installation](#installation)
1. [File Descriptions](#file_descriptions)
1. [Summary](#summary)
1. [Acknowledgements](#Acknowledgements)



## Project Overview <a name="#project_overview"></a>
This project is about discovering what is the best offer for starbucks customers, not just for the population as a whole but an individual personalized level.

This is a classifier that predicts customer response by entering customer and offer information.
The metric is the accuracy of the estimator.


### The motivation for the project
In the past, mass marketing such as commercials and advertisements was the mainstream, but with the spread of the Internet, it has become necessary to carry out promotional measures tailored to each customer.
In 1 to 1 marketing, by implementing promotions that are suitable for the customer, it is possible to make a good impression on the customer and at the same time optimize the business cost by appropriately distributing the promotion expenses.

Starbucks sends out an offer to users of the mobile app once every few days. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free).
Not all users receive the same offer.

The project goal is to combine transaction, demographic and offer data to determine which customer  respond best to which offer type.


### Prediction strategy
When Starbucks sends customers some discount promotions(BOGO and DISCOUNT), the reactions are classified into below:

view -> complete (success)
customers check the promotion and react on it. It's succes of the promotion offer.
view -> NOT complete (fail)
customers check the promotion but they don't use it.
Not view -> complete (no_contribute)
customers don't check the promotion but they use the promotion offer. the offer doesn't affect to the customer however the promotion costs.
Not view -> NOT complete (no_interest)
customers neither check and use the promotion offer.
From the perspective of business cost performance, Starbuckswant to increase success and decrease no_contribute. I'd like to create a classification ML program to predict how customers react to a certain offer.

![screenshot of the output](classifier_output.png)


## Installation <a name="installation"></a>
For running this project, the most important library is Python version of Anaconda Distribution. It installs all necessary packages for analysis and building models.
### version
Python 3.7.4  
pandas              0.25.1  
numpy               1.17.2  
seaborn              0.9.0  
matplotlib           3.1.1  
sklearn             0.21.3
=======
### Table of Content
1. [Project Overview](#project_overview)
1. [Installation](#installation)
1. [File Descriptions](#file_descriptions)
1. [Summary](#summary)
1. [Acknowledgements](#Acknowledgements)



## Project Overview <a name="#project_overview"></a>
This project is about discovering what is the best offer for starbucks customers, not just for the population as a whole but an individual personalized level.

This is a classifier that predicts customer response by entering customer and offer information.
The metric is the accuracy of the estimator.


### The motivation for the project
In the past, mass marketing such as commercials and advertisements was the mainstream, but with the spread of the Internet, it has become necessary to carry out promotional measures tailored to each customer.
In 1 to 1 marketing, by implementing promotions that are suitable for the customer, it is possible to make a good impression on the customer and at the same time optimize the business cost by appropriately distributing the promotion expenses.

Starbucks sends out an offer to users of the mobile app once every few days. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free).
Not all users receive the same offer.

The project goal is to combine transaction, demographic and offer data to determine which customer  respond best to which offer type.


### Prediction strategy
When Starbucks sends customers some discount promotions(BOGO and DISCOUNT), the reactions are classified into below:

view -> complete (success)  
&emsp;customers check the promotion and react on it. It's succes of the promotion offer.  
view -> NOT complete (fail)  
&emsp;customers check the promotion but they don't use it.  
Not view -> complete (no_contribute)  
&emsp;customers don't check the promotion but they use the promotion offer. the offer doesn't affect to the customer however the promotion costs.  
Not view -> NOT complete (no_interest)  
&emsp;customers neither check and use the promotion offer.  

From the perspective of business cost performance, Starbuckswant to increase success and decrease no_contribute. I'd like to create a classification ML program to predict how customers react to a certain offer.  

![screenshot of the output](classifier_output.png)


## Installation <a name="installation"></a>
For running this project, the most important library is Python version of Anaconda Distribution. It installs all necessary packages for analysis and building models.
### version
Python 3.7.4  
pandas              0.25.1  
numpy               1.17.2  
seaborn              0.9.0  
matplotlib           3.1.1  
sklearn             0.21.3
>>>>>>> e43008eaa406436230af4144dc92bce2eb792cee

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

<<<<<<< HEAD
3. Go to http://0.0.0.0:3001/
||||||| merged common ancestors
3. Go to http://0.0.0.0:3001/


## File Descriptions <a name="file_descriptions"></a>
### File and Structure
┣ `README.md` - this file  
┣ `Starbucks_Capstone_notebook.ipynb` - analyze data and draw figures  
┗ data  
&emsp;┣ `portfolio.json` - containing offer details  
&emsp;┣ `profile.json` - user profiles    
&emsp;┗ `transcript.json` - records for transactions and offers

### Dataset Overview
The dataset contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free).


`profile.json`
Rewards program users (17000 users x 5 fields)
- gender: (categorical) M, F, O, or null
- age: (numeric) missing value encoded as 118
- id: (string/hash)
- became_member_on: (date) format YYYYMMDD
- income: (numeric)

`portfolio.json` Offers sent during 30-day test period (10 offers x 6 fields)
- reward: (numeric) money awarded for the amount spent
- channels: (list) web, email, mobile, social
- difficulty: (numeric) money required to be spent to receive reward
- duration: (numeric) time for offer to be open, in days
- offer_type: (string) bogo, discount, informational
- id: (string/hash)

`transcript.json` Event log (306648 events x 4 fields)
- person: (string/hash)
- event: (string) offer received, offer viewed, transaction, offer completed
- value: (dictionary) different values depending on event type
- offer id: (string/hash) not associated with any "transaction"
- amount: (numeric) money spent in "transaction"
- reward: (numeric) money gained from "offer completed"
- time: (numeric) hours after start of test

## Summary <a name="#summary"></a>
The accuracy of the classifier is 0.6082.

### for the future improvement
This time, we made predictions only for coupon offers with discounts. If you want to measure the effect of information provision, it is possible to analyze it in time series together with transaction data.
I am simplifying the case where I receive the same offer multiple times. For example, if a person received the same offer three times, saw it twice, and used it once, it was classified as success. In order to improve the prediction accuracy, it is necessary to consider a data storage method that correlates at what time the coupon was sent and when it was opened.
In order to make the UX more considerate of marketing, when inputting the offer conditions, it may be possible to extract the customer list that responds to the offer in descending order of probability.



## Acknowledgements <a name="acknowledgements"></a>
This is an assignment in Data Scientist Nanodegree program in Udacity.
I appreciate the teachers and mentors who encourage me to brush up the skills as a data scientist.
Also, I really thank to Starbucks, which provides me a great opportunity to analyze the data based on the real business.
=======

## File Descriptions <a name="file_descriptions"></a>
### File and Structure
┣ `README.md` - this file  
┣ `Starbucks_Capstone_notebook.ipynb` - analyze data and draw figures  
┣ `classifier_output.png` - output image 
┣ data  
┃&emsp;┣ `clean_data.db` - clean data after running data_clean.py  
┃&emsp;┣ `data_clean.py` - python to clean data  
┃&emsp;┣ `portfolio.json` - containing offer details   
┃&emsp;┣ `profile.json` - user profiles      
┃&emsp;┗ `transcript.json` - records for transactions and offers  
┣ data_to_estimate  
┃&emsp;┣ `estimate_data.csv` - sample data to predict (can replace or modify to yours)  
┃&emsp;┗ `run_estimator.py` - python to run the estimator  
┗ data  
&emsp;┣ `classifier.pkl` - classifier after running estimator.py  
&emsp;┗ `estimator.py` - python to create the classifier


### Dataset Overview
The dataset contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free).


`profile.json`
Rewards program users (17000 users x 5 fields)
- gender: (categorical) M, F, O, or null
- age: (numeric) missing value encoded as 118
- id: (string/hash)
- became_member_on: (date) format YYYYMMDD
- income: (numeric)

`portfolio.json` Offers sent during 30-day test period (10 offers x 6 fields)
- reward: (numeric) money awarded for the amount spent
- channels: (list) web, email, mobile, social
- difficulty: (numeric) money required to be spent to receive reward
- duration: (numeric) time for offer to be open, in days
- offer_type: (string) bogo, discount, informational
- id: (string/hash)

`transcript.json` Event log (306648 events x 4 fields)
- person: (string/hash)
- event: (string) offer received, offer viewed, transaction, offer completed
- value: (dictionary) different values depending on event type
- offer id: (string/hash) not associated with any "transaction"
- amount: (numeric) money spent in "transaction"
- reward: (numeric) money gained from "offer completed"
- time: (numeric) hours after start of test

## Summary <a name="#summary"></a>
The accuracy of the classifier is 0.6082.

### for the future improvement
This time, we made predictions only for coupon offers with discounts. If you want to measure the effect of information provision, it is possible to analyze it in time series together with transaction data.
I am simplifying the case where I receive the same offer multiple times. For example, if a person received the same offer three times, saw it twice, and used it once, it was classified as success. In order to improve the prediction accuracy, it is necessary to consider a data storage method that correlates at what time the coupon was sent and when it was opened.
In order to make the UX more considerate of marketing, when inputting the offer conditions, it may be possible to extract the customer list that responds to the offer in descending order of probability.



## Acknowledgements <a name="acknowledgements"></a>
This is an assignment in Data Scientist Nanodegree program in Udacity.
I appreciate the teachers and mentors who encourage me to brush up the skills as a data scientist.
Also, I really thank to Starbucks, which provides me a great opportunity to analyze the data based on the real business.
>>>>>>> e43008eaa406436230af4144dc92bce2eb792cee
