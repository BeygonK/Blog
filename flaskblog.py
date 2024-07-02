from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b936b20e204230db5378a51973d74fa4'

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

if __name__ == '__main__':
    app.run(debug=True)