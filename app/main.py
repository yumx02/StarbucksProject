import sys
from flask import Flask, render_template,request
import requests
import pandas as pd
import numpy as np

import sys
sys.path.append('..')
import run_estimator

def clean_imput_data(result):
    age=int(result["age"])
    income=int(result["income"])
    became_member_on=int(result["became_member_on"])
    gender=str(result["gender"])
    offer_type=str(result["offer_type"])
    difficulty=int(result["difficulty"])
    reward=int(result["reward"])
    duration=int(result["duration"])
    channel=str(result["channel"])
    info=0

    #channels
    mobile = 0
    email = 0
    web = 0
    social = 0
    if channel == "mobile":
        mobile = 1
    if channel == "email":
        email = 1
    if channel == "web":
        web = 1
    if channel == "social":
        social = 1

    #offer_type
    bogo = 0
    discount = 0
    if offer_type == "bogo":
        bogo = 1
    if offer_type == "discount":
        discount = 1

    #gender
    M = 0
    F = 0
    O = 0
    if gender == "m":
        M = 1
    if gender == "f":
        F = 1
    if gender == "o":
        O = 1

    imput_data = [mobile,email,web,social,difficulty,reward,duration,bogo,discount,info,age,income,became_member_on,M,F,O]
    imput_data = pd.DataFrame(np.array([imput_data,imput_data]))
    return imput_data







app = Flask(__name__)
#indexページ(フォーム画面)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output/', methods = ['POST'])
def output():
    result  = request.form
    imput_data = clean_imput_data(result)

    y_pred = run_estimator.main(imput_data)
    y_pred = y_pred.iloc[-1]

    y_pred_values = y_pred.values.tolist()
    y_pred_index = y_pred.index.tolist()

    success = y_pred_values[0]
    fail = y_pred_values[1]
    no_cont = y_pred_values[2]
    no_int = y_pred_values[3]

    if success == 1:
        predic = "success (they may check the coupon and use it)"
    if fail == 1:
        predic = "fail (they may see the coupon but doesn't use)"
    if no_cont == 1:
        predic = "no contribution (they may not see the coupon but use)"
    if no_int == 1:
        predic = "no intetest(they may neither see and use the coupon)"
    else:
        predict = "unknown(please try again with other conditions)"

    return render_template("output.html",y_pred = y_pred,y_pred_values = y_pred_values, y_pred_index = y_pred_index, result=result,predic=predic)

if __name__ == '__main__':
    # app.debug = False#デバッグモードTrueにすると変更が即反映される
    app.debug = True#デバッグモードTrueにすると変更が即反映される
    app.run()
