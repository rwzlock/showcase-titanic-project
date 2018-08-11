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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///titanic_db.sqlite" 

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

 # Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()

# import warnings
# warnings.simplefilter('ignore')

# %matplotlib inline
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read train and test csv files
train_data_cleaned_v2 = pd.read_csv('Resources/AG_train-test_v2.csv')

# select the columns will be used in testing
X = train_data_cleaned_v2.drop('Survived', axis = 1)
y = train_data_cleaned_v2['Survived']

X.drop('Unnamed: 0', axis = 1, inplace=True)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)


# Support vector machine linear classifier
from sklearn.svm import SVC
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# import pickle to store model
import pickle
s = pickle.dumps(model)
model = pickle.loads(s)

# import joblib to load model
from sklearn.externals import joblib
joblib.dump(model, 'model.pkl') 
model = joblib.load('model.pkl') 

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
    results = db.session.query(User.name, User.age).all()
    
    name = [result[0] for result in results]
    age = [int(result[1]) for result in results]

    plot_trace = {
        "x": name,
        "y": age,
        "type": "bar"
    }
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        newUser.append([2,0,20,1,1,1,0])
        
        userName = request.form["userName"]
        userPclass = request.form["userPclass"]
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

        if userEmbarked == "C":
            newUser[0][3]= 0
        if userTicket == "Q":
            newUser[0][3]= 1
        else:
            newUser[0][3]= 2


        if userGender == "Male":
            newUser[0][1]= 0
        else:
            newUser[0][1]= 1

        if request.method == "POST":
            userName = request.form["userName"]
            userEmbarked = request.form["userEmbarked"]
            if userEmbarked == "C":
                newUser[0][3]= 0
            if userTicket == "Q":
                newUser[0][3]= 1
            else:
                newUser[0][3]= 2

            userAge = request.form["userAge"]

            prediction = model.predict(newUser)

            print(prediction)
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
            return jsonify(plot_trace)
            
#         prediction = model.predict(newUser)
        
#         return redirect("/result", code=302)
#         # return jsonify(newUser)

#     return render_template("form.html")


@app.route("/result")
def pals():
    prediction = model.predict(newUser)

    if prediction[0] == 1:
        return render_template('result.html', prediction = "Survive", result_list = newUser )
    else:
        return render_template('result.html', prediction = "Die", result_list = newUser )

@app.route("/plot")
def plot():
    
    results = db.session.query(User.name,User.pclass,User.sex, User.age,User.sibsp, User.parch, User.fare, User.embarked, User.survived).all()
    
    name = [result[0] for result in results]
    age = [result[1] for result in results]
    sex = [result[2] for result in results]

    user_data = [{

        "name": name,
        "age": age,
        "sex": sex,

    }]

    return jsonify(user_data)
#Run the app. debug=True is essential to be able to rerun the server any time changes are saved to the Python file
if __name__ == "__main__":
    app.run(debug=True, port=5035)