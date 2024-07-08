"""This module handles routing
to specific pages
"""

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import CreatePost

posts = Blueprint('posts', __name__)

# dummy data
# posts = [{"title": "My Updated Post", "content": "My first updated post!\r\n\r\nThis is exciting!", "user_id": 1}, {"title": "A Second Post", "content": "This is a post from a different user...", "user_id": 2}]
  
@posts.route("/post/create", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('create.html', title='New Post',
                           form=form, legend='Create Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    """Fetch single post
    matching the id
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    """Update a user post
    only if user is logged in
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post update successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create.html', title='Update Post',
                           form=form, legend='Update Post')
    
    
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'danger')
    return redirect(url_for('main.home'))
    