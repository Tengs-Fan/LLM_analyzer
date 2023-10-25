from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
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

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
