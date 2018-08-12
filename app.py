# import necessary libraries
import os
import numpy as np
import pandas as pd
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

#################################################
# Database Setup
#################################################
# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/titanic_db.sqlite" 

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    pclass = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    age = db.Column(db.Integer)
    sibsp = db.Column(db.Integer)
    parch = db.Column(db.Integer)
    fare = db.Column(db.Integer)
    embarked = db.Column(db.Integer)
    survived = db.Column(db.Integer)
    
    def __init__(self, name, pclass, sex, age, sibsp, parch, fare, embarked, survived ):
        self.name = name
        self.pclass = pclass
        self.sex = sex
        self.age = age
        self.sibsp = sibsp
        self.parch = parch
        self.fare = fare
        self.embarked = embarked
        self.survived = survived
        

    def __repr__(self):
        return '<User %r>' % (self.name)
    
class Passenger(db.Model):
    __tablename__ = 'train_data'
    db.reflect()
   

 # Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
#     db.drop_all()
    db.create_all()

# import warnings
# warnings.simplefilter('ignore')

# %matplotlib inline
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import joblib to load model
from sklearn.externals import joblib
knn_model = joblib.load('Resources/models/knn.pkl') 
knn_scaler_model = joblib.load('Resources/models/knn_scaler.pkl') 

# create new User list to store newUser data
newUser=[]
newUser.append([3,0,35,0,0,1,1])
newUser = knn_scaler_model.transform(newUser)

# make prediction with new user data
prediction = knn_model.predict(newUser)
print(prediction)


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
                
        userName = request.form["userName"]
        userPclass = request.form["userPclass"]
        userEmbarked = request.form["userEmbarked"]
        userAge = request.form["userAge"]
        userTicket= request.form["userTicket"]
        userGender= request.form["userGender"]
        
        if userGender.lower() == "male":
            newUser[0][1]= 0
        else:
            newUser[0][1]= 1

        newUser[0][2]= int(userAge)
        
        if userEmbarked.lower() == "c":
            newUser[0][3]= 0
        if userEmbarked.lower() == "q":
            newUser[0][3]= 1
        if userEmbarked.lower() == "s":
            newUser[0][3]= 2

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

        prediction = knn_model.predict(newUser)

        user = User(name=userName, pclass = userPclass, sex = newUser[0][1], age=userAge, sibsp = 0, parch = 0, fare = newUser[0][5], embarked = newUser[0][3], survived = int(prediction[0]))
        db.session.add(user)
        db.session.commit()

        results = db.session.query(User.name,User.pclass,User.sex, User.age,User.sibsp, User.parch, User.fare, User.embarked, User.survived).all()

        name = [result[0] for result in results]
        pclass = [int(result[1]) for result in results]
        sex = [int(result[2]) for result in results]
        age = [int(result[3]) for result in results]
        sibsp = [int(result[4]) for result in results]
        parch = [int(result[5]) for result in results]
        fare = [result[6] for result in results]
        embarked = [result[7] for result in results]
        survived = [int(result[8]) for result in results]


        plot_trace = {
            "name": name,
            "Pclass": pclass,
            "Gender": sex,
            "Age": age,
            "Sibsp": sibsp,
            "Parch": parch,
            "fare": age,
            "Embarked": embarked,
            "Survived": survived,

        }
        
        return redirect("/result", code=302)

    return render_template("form.html")


@app.route("/result")
def pals():
    prediction = knn_model.predict(newUser)

    if prediction[0] == 1:
        return render_template('result.html', prediction = "Survive", result_list = newUser )
    else:
        return render_template('result.html', prediction = "Die", result_list = newUser )

@app.route("/embarked")
def embarked():
    
    #Same query method as used in the /plot route
    results = db.session.query(User.embarked,User.survived).all()
    embarkedlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    embarkedes = list(set(embarkedlist))
    embarkedcounts = []
    
    for embarked in embarkedes:
        counter = 0
        for x in range(0, len(embarkedlist)):
            if(str(embarkedlist[x]) == str(embarked) ):
                counter=counter+1
        embarkedcounts.append(counter)
    
    embarked_trace = {
        "x": ["Cherbourg","Queenstown","Southampton"],
        "y": embarkedcounts,
        "type": "bar"
    }
    return jsonify(embarked_trace)

@app.route("/gender")
def gender():
    
    #Same query method as used in the /plot route
    results = db.session.query(User.sex,User.survived).all()
    sexlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    sexes = list(set(sexlist))
    sexcounts = []
    
    for sex in sexes:
        counter = 0
        for x in range(0, len(sexlist)):
            if(str(sexlist[x]) == str(sex) ):
                counter=counter+1
        sexcounts.append(counter)
    
    sex_trace = {
        "x": ["Male","Female"],
        "y": sexcounts,
        "type": "bar"
    }
    return jsonify(sex_trace)

@app.route("/plots")
def plots():
    
    #Same query method as used in the /plot route
    results = db.session.query(Passenger.Sex, Passenger.Survived).all()
    sexlist = [result[0] for result in results]
    survivedlist = [result[1] for result in results]
    sexes = list(set(sexlist))
    sexcounts = []
    
    for sex in sexes:
        counter = 0
        for x in range(0, len(sexlist)):
            if(str(sexlist[x]) == str(sex) ):
                counter=counter+1
        sexcounts.append(counter)
    
    sex_trace = {
        "x": ["Male","Female"],
        "y": sexcounts,
        "type": "bar"
    }
    return jsonify(sex_trace)

#Run the app. debug=True is essential to be able to rerun the server any time changes are saved to the Python file
if __name__ == "__main__":
    app.run(debug=True, port=5015)