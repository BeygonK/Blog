from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
def home():
    """This is for home page"""

    posts = Post.query.all()
    return render_template("articles.html",
                           posts=posts)