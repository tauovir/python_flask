#from flask import Flask,render_template
from flask import Flask, redirect, url_for,request,render_template,flash,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

with open('config.json','r') as c:
    params = json.load(c)["params"]

isLocalServer = params['local_server']
app = Flask(__name__)
app.secret_key = "Ignou@555355"
# Mail Configuraion
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = "465",
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "roman.seth707@gmail.com",
    MAIL_PASSWORD = "roman@555355"

)
mail = Mail(app)
if(isLocalServer):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    print("local")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    print("production")

db = SQLAlchemy(app)
# db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    sub_title = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)
    image_url = db.Column(db.String(120), unique=False, nullable=False)
    created_at = db.Column(db.String(120), nullable=True)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)
    created_at = db.Column(db.String(120), nullable=True)

@app.route("/")
def hello():
    post = Posts.query.all()
    return render_template("index.html", params = params, posts = post)

@app.route("/contact", methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email_add = request.form['email']
        phone_num = request.form['phone']
        message = request.form['message']
        enrty = Contacts(name = name, email = email_add, phone = phone_num,message = message,  created_at = datetime.now())
        db.session.add(enrty)
        db.session.commit()
        flash("Thank you for Contact us")
        mail.send_message(
            'New Message from',
            sender= email_add,
            recipients= "roman.seth707@gmail.com",
            body = message 
        )
        return redirect(url_for('contact'))

    else:
        return render_template("contact.html", params = params)

@app.route("/about")
def about():
    return render_template("about.html", params = params)


@app.route("/post/<string:post_slug>", methods = ['GET'])
def getPost(post_slug):
    print(post_slug)
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template("post.html", params = params, post = post)


# @app.route("/post")
# def post():
#     return render_template("post.html", params = params)

@app.route("/dashboard")
def dashboard():
    post = Posts.query.all()
    return render_template("dashboard.html", params = params, posts = post)





@app.route("/add_post",methods = ['GET','POST'])
def addPost():
    # if 'username' not in session and session['username'] != params['admin_user']:
    #     return render_template("login.html", params = params)

    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        slug = request.form['slug']
        content = request.form['content']
        enrty = Posts(title = title, sub_title = subtitle, slug = slug,content = content,  created_at = datetime.now())
        db.session.add(enrty)
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return render_template("add_form.html", params = params, post = post)


@app.route("/post/edit/<string:postId>",methods = ['GET','POST'])
def editPost(postId):
    # if 'username' not in session and session['username'] != params['admin_user']:
    #     return render_template("login.html", params = params)

    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        slug = request.form['slug']
        content = request.form['content']
        ## Edit Post
        post = Posts.query.filter_by(id = postId).first()
        post.title = title
        post.sub_title = subtitle
        post.slug = slug 
        post.content = content
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        post = Posts.query.filter_by(id = postId).first()
        return render_template("edit_form.html", params = params, post = post)
    

@app.route("/post/delete/<string:postId>",methods = ['GET'])
def deletePost(postId):
    if request.method == 'GET':
        print(postId)
        Posts.query.filter_by(id=postId).delete()
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
         return redirect(url_for('contact'))


@app.route("/logout", methods = ['GET','POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/login", methods = ['GET','POST'])
def login():
    if 'username' in session and session['username'] == params['admin_user']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (username == params['admin_user'] and password == params['admin_pass']):
            session['username'] = username
            flash("You have successfully logedin")
            return redirect(url_for('dashboard'))
        else:
            flash("Access denied")
            return render_template("login.html", params = params)

    else:
        return render_template("login.html", params = params)


app.run(debug = True)