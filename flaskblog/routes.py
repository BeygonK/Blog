from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [{"title": "My Updated Post", "content": "My first updated post!\r\n\r\nThis is exciting!", "user_id": 1}, {"title": "A Second Post", "content": "This is a post from a different user...", "user_id": 2}]


@app.route("/")
def home():
    return render_template("articles.html",
                           posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created successfuly!", "success")
        return redirect(url_for('home'))
    return render_template('register.html',
                           title='Register',
                           form=form) 


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Check your email or password!", "danger")
        return redirect(url_for('home'))
    return render_template('login.html',
                           title='Login',
                           form=form)  