# import necessary libraries
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

import warnings
warnings.simplefilter('ignore')

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import joblib to load model
from sklearn.externals import joblib
model = joblib.load('Resources/models/knn.pkl')
scaler = joblib.load('Resources/models/knn_scaler.pkl')

# run X_test to see predictions
predictions = model.predict(X_test)

# create new User list to store newUser data
newUser=[]
newUser.append([3,0,35,0,0,1,1])

# make prediction with new user data
prediction = model.predict(newUser)
print(prediction)


@app.route("/")
def index():
    predictions_dict = {

    }
    for x in predictions:
        count = 0
        if x == 0:
            predictions_dict["Prediction"] = "Not Survived"
        else:
            predictions_dict["Prediction"] = "Survived"    
    return render_template('index.html', predictions = predictions_dict )

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        newUser.append([2,0,20,1,1,1,0])
        
        userEmbarked = request.form["userEmbarked"]
        userAge = request.form["userAge"]
        userTicket= request.form["userTicket"]
        userGender= request.form["userGender"]
        # userName[0] = request.form["userName"]
        # newUser.append(userName)
        # userAge = request.form["userAge"]
        # newUser.append(userAge)
        # userTicket = request.form["userTicket"]
        # newUser.append(userTicket)
        
        newUser[0][6]= int(userEmbarked)
        newUser[0][2]= int(userAge)
        
        if userTicket == "Basic Economy":
            newUser[0][5]= 0
        if userTicket == "Economy":
            newUser[0][5]= 1
        if userTicket == "Middle Class":
            newUser[0][5]= 2
        if userTicket == "Business":
            newUser[0][5]= 3
        else:
            newUser[0][5]= 4


        if userGender == "male":
            newUser[0][1]= 0
        else:
            newUser[0][1]= 1
        prediction = model.predict(newUser)
        
        return redirect("/result", code=302)
        # return jsonify(newUser)

    return render_template("form.html")


@app.route("/result")
def pals():
    prediction = model.predict(newUser)

    if prediction[0] == 1:
        return render_template('result.html', prediction = "Survive", result_list = newUser )
    else:
        return render_template('result.html', prediction = "Die", result_list = newUser )

#Run the app. debug=True is essential to be able to rerun the server any time changes are saved to the Python file
if __name__ == "__main__":
    app.run(debug=True, port=5010)