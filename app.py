from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user import User  # Import the User class from user.py
from db import mongo 

app = Flask(__name__)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Replace the following line with code to fetch the user from your database
        user = User(username, 'password')  # This is just an example, fetch the actual user from your database
        if user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reddit_post')
def reddit_comments():
    post = mongo.find_post('17a1ph8')
    comments = mongo.find_comments_by_post('17a1ph8')  #
    return render_template('reddit.html', post=post, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
