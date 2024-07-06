"""This module handles routing
to specific pages
"""

from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, bcrypt, db
import os
from PIL import Image
import secrets
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreatePost
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# dummy data
# posts = [{"title": "My Updated Post", "content": "My first updated post!\r\n\r\nThis is exciting!", "user_id": 1}, {"title": "A Second Post", "content": "This is a post from a different user...", "user_id": 2}]


@app.route("/")
def home():
    """This is for home page"""

    posts = Post.query.all()
    return render_template("articles.html",
                           posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """This is for registration route"""
    
    if current_user.is_authenticated: # check authentication
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Handles login functionality"""
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',
                           title='Login',
                           form=form)  
    
@app.route("/logout")
def logout():
    """Handles logout"""
    
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    """This method saves picture
    by first generating a random string
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125) # resize the image
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Handles the  users account"""
    
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account',
                           form=form,
                           image_file=image_file)
    
    

@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new post and save 
    it in database
    """
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create.html', title='New Post', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    """Fetch single post
    matching the id
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)