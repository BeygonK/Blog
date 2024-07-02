from flask import Flask, render_template, url_for
app = Flask(__name__)


posts = [{"title": "My Updated Post", "content": "My first updated post!\r\n\r\nThis is exciting!", "user_id": 1}, {"title": "A Second Post", "content": "This is a post from a different user...", "user_id": 2}]


@app.route("/")
def home():
    return render_template("articles.html", posts=posts)


if __name__ == '__main__':
    app.run(debug=True)