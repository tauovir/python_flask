#from flask import Flask,render_template
from flask import Flask, redirect, url_for,request,render_template,flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "Ignou@555355"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/flask'
db = SQLAlchemy(app)
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    created_at = db.Column(db.String(120), nullable=True)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/datatable")
def dataTable():
    return render_template("pages/tables/data.html")
    
@app.route("/form")
def form():
    return render_template("pages/forms/general.html")


@app.route("/register", methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dict1 = {'name':name,'emial':email,'password':password}
        enrty = Users(name = name, email = email, password = password, created_at = datetime.now())
        db.session.add(enrty)
        db.session.commit()
        flash("You successfully Register")
        return redirect(url_for('hello'))

    else:
        return render_template("pages/examples/register.html")




app.run(debug = True)